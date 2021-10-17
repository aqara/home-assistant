import asyncio
import json
import logging
from typing import Optional, Union

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo, Entity
from rocketmq.client import PushConsumer, RecvMessage

from .aiot_cloud import AiotCloud, APP_ID, KEY_ID, APP_KEY
from .aiot_mapping import (
    MK_MAPPING_PARAMS,
    MK_INIT_PARAMS,
    MK_RESOURCES,
    MK_HASS_NAME,
    AIOT_DEVICE_MAPPING,
)
from .const import DOMAIN, HASS_DATA_AIOT_MANAGER, CONF_DEBUG


_LOGGER = logging.getLogger(__name__)


class AiotDevice:
    def __init__(self, **kwargs):
        self.did = kwargs.get("did")
        self.parent_did = kwargs.get("parentDid")
        self.model = kwargs.get("model")
        self.model_type = kwargs.get("modelType")
        self.device_name = kwargs.get("deviceName")
        self.state = kwargs.get("state")
        self.timezone = kwargs.get("timeZone")
        self.firmware_version = kwargs.get("firmwareVersion")
        self.create_time = kwargs.get("createTime")
        self.update_time = kwargs.get("updateTime")
        self.platforms = None
        for device in AIOT_DEVICE_MAPPING:
            if self.model in device:
                self.platforms = device['params']
                break
        self.children = []

    @property
    def is_supported(self):
        return self.platforms is not None


class AiotEntityBase(Entity):
    _channel = None
    _device = None
    _res_params = None
    _supported_resources = None
    _aiot_manager = None

    _attr_lqi = None
    _attr_chip_temperature = None
    _attr_voltage = None
    _attr_fw_ver = None

    def __init__(self, hass, device, res_params, type_name, channel=None, **kwargs):
        self._device = device
        self._res_params = res_params
        self._supported_resources = []
        [
            self._supported_resources.append(v[0].format(channel))
            for k, v in res_params.items()
        ]
        self._channel = channel

        self.hass = hass
        self._attr_name = device.device_name
        self._attr_should_poll = False
        self._attr_unique_id = (
            f"{DOMAIN}.{type_name}_0x{device.did.split('.', 1)[1]}_{kwargs.get('hass_attr_name')}"
        )
        self.entity_id = f"{DOMAIN}.0x{device.did.split('.', 1)[1]}_{kwargs.get('hass_attr_name')}"
        if channel:
            self._attr_unique_id = f"{self._attr_unique_id}_{channel}"
            self.entity_id = f"{self.entity_id}_{channel}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device.did)},
            name=self._attr_name,
            model=device.model,
            manufacturer=(device.model or "Lumi").split(".", 1)[0].capitalize(),
            sw_version=device.firmware_version,
        )
        self._attr_supported_features = kwargs.get("supported_features")
        self._attr_unit_of_measurement = kwargs.get("unit_of_measurement")
        self._attr_device_class = kwargs.get("device_class")

        self._aiot_manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]

    def debug(self, message: str):
        """ deubug function """
        self._aiot_manager.debug(f"{self.entity_id}: {message}")

    @property
    def channel(self) -> int:
        return self._channel

    @property
    def supported_resources(self) -> list:
        return self._supported_resources

    @property
    def device(self) -> AiotDevice:
        return self._device

    @property
    def lqi(self):
        """Return the signal strength of zigbee """
        return self._attr_lqi

    @property
    def chip_temperature(self):
        """Return the chip temperature."""
        return self._attr_chip_temperature

    @property
    def voltage(self):
        """Return battery voltage."""
        return self._attr_voltage

    @property
    def fw_ver(self):
        """Return firmware version."""
        return self._attr_fw_ver

    def get_res_id_by_name(self, res_name):
        return self._res_params[res_name][0].format(self._channel)

    async def async_set_res_value(self, res_name, value):
        """设置资源值"""
        res_id = self.get_res_id_by_name(res_name)
        if 'verbose' in self._aiot_manager.debug_option:
            self.debug("async_set_res_value {} {} {}".format(self.device.did, res_id, value))
        return await self._aiot_manager.session.async_write_resource_device(
            self.device.did, res_id, value
        )

    async def async_fetch_res_values(self, *args):
        """获取资源值"""
        res_ids = []
        if len(args) > 0:
            res_ids = args
        else:
            [
                res_ids.append(self.get_res_id_by_name(k))
                for k, v in self._res_params.items()
            ]
        return await self._aiot_manager.session.async_query_resource_value(
            self.device.did, res_ids
        )

    async def async_update(self):
        resp = await self.async_fetch_res_values()
        if resp:
            for x in resp:
                await self.async_set_attr(x["resourceId"], x["value"], write_ha_state=False)

    async def async_set_resource(self, res_name, attr_value):
        """设置aiot resource的值"""
        tup_res = self._res_params.get(res_name)
        if tup_res:
            res_value = attr_value
            current_value = getattr(self, tup_res[1])
            resp = None
            if 'verbose' in self._aiot_manager.debug_option:
                self.debug("set {} with value {} on {}".format(self.device.did, res_value, res_name))
            if current_value != attr_value:
                res_value = self.convert_attr_to_res(res_name, attr_value)
                resp = await self.async_set_res_value(res_name, res_value)
            # TODO 这里需要判断是否调用成功，再进行赋值
            self.__setattr__(tup_res[1], attr_value)
            self.async_write_ha_state()
            return resp

    async def async_set_attr(self, res_id, res_value, write_ha_state=True):
        """设置ha attr的值"""
        res_name = next(
            k
            for k, v in self._res_params.items()
            if v[0].format(self.channel) == res_id
        )
        tup_res = self._res_params.get(res_name)
        attr_value = self.convert_res_to_attr(res_name, res_value)
        current_value = getattr(self, tup_res[1], None)
        if 'verbose' in self._aiot_manager.debug_option:
            self.debug("set value {} current: {} write: {}".format(attr_value, current_value, write_ha_state))
        if current_value != attr_value:
            self.__setattr__(tup_res[1], attr_value)
            if write_ha_state:
                self.async_write_ha_state()  # 初始化的时候不能执行这句话，会创建其他乱七八糟的对象

    async def async_device_connection(self, Open=False):
        """ enable/disable device connection """
        if 'verbose' in self._aiot_manager.debug_option:
            self.debug("async_device_connection {}".format(self.device.did))
        if Open:
            return await self._aiot_manager.session.async_write_device_openconnect(
                self.device.did
            )
        return await self._aiot_manager.session.async_write_device_closeconnect(
            self.device.did
        )

    async def async_infrared_learn(self, Enable=False, timelength=20):
        """ enable/disable infrared learn """
        if Enable:
            return await self._aiot_manager.session.async_write_ir_startlearn(
                self.device.did, time_length=timelength
            )
        return await self._aiot_manager.session.async_write_ir_cancellearn(
            self.device.did
        )

    async def async_received_learnresult(self, keyid):
        """ receive infrared learn result """
        return await self._aiot_manager.session.async_query_ir_learnresult(
            self.device.did, keyid
        )

    def convert_attr_to_res(self, res_name, attr_value):
        """从attr转换到res"""
        return attr_value

    def convert_res_to_attr(self, res_name, res_value):
        """从res转换到attr"""
        return res_value


class AiotToggleableEntityBase(AiotEntityBase):
    def __init__(self, hass, device, res_params, type_name, channel, **kwargs):
        super().__init__(hass, device, res_params, type_name, channel=channel, **kwargs)
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs):
        await self.async_set_resource("toggle", True)

    async def async_turn_off(self, **kwargs):
        await self.async_set_resource("toggle", False)

    def convert_attr_to_res(self, res_name, attr_value):
        if res_name == "toggle":
            # res_value：bool
            return "1" if attr_value else "0"
        return super().convert_attr_to_res(res_name, attr_value)

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "toggle":
            # res_value：0或1，字符串
            return res_value == "1"
        return super().convert_res_to_attr(res_name, res_value)


class AiotMessageHandler:
    def __init__(self, loop):
        self._loop = loop
        self._consumer = PushConsumer(APP_ID)
        self._consumer.set_namesrv_addr("3rd-subscription.aqara.cn:9876")
        self._consumer.set_session_credentials(KEY_ID, APP_KEY, "")

    def start(self, callback):
        def consumer_callback(msg: RecvMessage):
            asyncio.set_event_loop(self._loop)
            asyncio.run_coroutine_threadsafe(
                callback(json.loads(str(msg.body, "utf-8"))),
                self._loop,
            )

        self._consumer.subscribe(APP_ID, consumer_callback)
        self._consumer.start()

    def stop(self):
        self._consumer.shutdown()


class AiotManager:
    # Aiot会话
    _session: AiotCloud = None

    # 所有设备
    _all_devices: Optional[Union[str, AiotDevice]]  = {}

    # 所有在HA中管理的设备
    _managed_devices: Optional[Union[str, AiotDevice]] = {}

    # 配置对象和设备的对应关系，1：N
    _entries_devices: Optional[Union[str, list]] = {}

    # 所有配置对象
    _config_entries: Optional[Union[str, ConfigEntry]]  = {}

    # 设备和实体的对应关系，1：N
    _devices_entities: Optional[Union[str, list]] = {}

    # 插件不支持的设备列表
    _unsupported_devices: Optional[list] = []

    debug_option = ''

    def __init__(self, hass: HomeAssistant, session: AiotCloud):
        self._hass = hass
        self._session = session
        self._msg_handler = AiotMessageHandler(asyncio.get_event_loop())
        self._msg_handler.start(self._msg_callback)
        self._options = None

    def debug(self, message: str):
        """ deubug function """
        if self._options is None:
            self._options = self._session.get_options()
        self.debug_option = self._options.get('debug', '')
        if 'true' in self.debug_option:
            _LOGGER.error(f"{message}")

    @property
    def session(self) -> AiotCloud:
        """与Aiot建立的会话"""
        return self._session

    @property
    def all_devices(self) -> Optional[list]:
        """获取Aiot Cloud上的所有设备"""
        return self._all_devices.values()

    @property
    def unmanaged_gateways(self) -> Optional[list]:
        """获取HA为管理的网关设备"""
        gateways = []
        [
            gateways.append(x)
            for x in self._all_devices.values()
            if x.model_type in (1, 2) and x.did not in self._managed_devices.keys()
        ]
        return gateways

    @property
    def unsupported_devices(self) -> Optional[list]:
        """插件不支持的设备列表"""
        devices = []
        [devices.append(x) for x in self._all_devices.values() if not x.is_supported]
        return devices

    async def _msg_callback(self, msg):
        """消息推送格式，见https://opendoc.aqara.cn/docs/%E4%BA%91%E5%AF%B9%E6%8E%A5%E5%BC%80%E5%8F%91%E6%89%8B%E5%86%8C/%E6%B6%88%E6%81%AF%E6%8E%A8%E9%80%81/%E6%B6%88%E6%81%AF%E6%8E%A8%E9%80%81%E6%A0%BC%E5%BC%8F.html"""
        if msg.get("msgType"):
            # 属性消息，resource_report
            if 'msg' in self.debug_option:
                self.debug("msgType {}".format(msg['data']))
            for x in msg["data"]:
                entities = self._devices_entities.get(x["subjectId"])
                if entities:
                    for entity in entities:
                        if x["resourceId"] in entity.supported_resources:
                            await entity.async_set_attr(x["resourceId"], x["value"])
        elif msg.get("eventType"):
            if 'msg' in self.debug_option:
                self.debug("eventType {}".format(msg['data']))
            # 事件消息
            if msg["eventType"] == "gateway_bind":  # 网关绑定
                pass
            elif msg["eventType"] == "subdevice_bind" or msg['cause'] == 11:  # 子设备绑定
                pass
            elif msg["eventType"] == "gateway_unbind":  # 网关解绑
                pass
            elif msg["eventType"] == "unbind_sub_gw":  # 子设备解绑
                pass
            elif msg["eventType"] == "gateway_online":  # 网关在线
                pass
            elif msg["eventType"] == "gateway_offline":  # 网关离线
                pass
            elif msg["eventType"] == "subdevice_online":  # 子设备在线
                pass
            elif msg["eventType"] == "subdevice_offline":  # 子设备离线
                pass
            else:  # 其他事件暂不处理
                pass
        else:
            _LOGGER.warn("unknown msg: {}".format(msg))

    async def async_refresh_all_devices(self):
        """获取Aiot所有设备"""
        self._all_devices = {}
        results = await self._session.async_query_all_devices_info()
        [self._all_devices.setdefault(x["did"], AiotDevice(**x)) for x in results]

    async def async_add_devices(
        self,
        config_entry: ConfigEntry,
        devices: Optional[list],
        auto_add_sub_devices=False,
    ):
        await self.async_refresh_all_devices()  # 刷新一次所有设备列表
        self._entries_devices.setdefault(config_entry.entry_id, [])
        self._config_entries[config_entry.entry_id] = config_entry
        for device in devices:
            # 这里看情况检查did是否已经存在，理论上来说应该不会重复，现在代码未做重复判断
            if device.is_supported:
                self._managed_devices[device.did] = device
                self._entries_devices[config_entry.entry_id].append(device.did)
                if auto_add_sub_devices and device.model_type == 1:
                    sub_devices = []
                    [
                        sub_devices.append(x)
                        for x in self.all_devices
                        if x.parent_did == device.did
                    ]
                    for sub_device in sub_devices:
                        if sub_device.is_supported:
                            device.children.append(sub_device)
                            self._managed_devices[sub_device.did] = sub_device
                            self._entries_devices[config_entry.entry_id].append(
                                sub_device.did
                            )
                        else:
                            _LOGGER.warn(
                                f"Aqara device is not supported. Deivce model is '{sub_device.model}'."
                            )
            else:
                _LOGGER.warn(
                    f"Aqara device is not supported. Deivce model is '{device.model}'."
                )
                continue

    async def async_forward_entry_setup(self, config_entry: ConfigEntry):
        devices_in_entry = self._entries_devices[config_entry.entry_id]
        platforms = []
        for x in devices_in_entry:
            if self._managed_devices[x].is_supported:
                for i in range(len(self._managed_devices[x].platforms)):
                    platforms.extend(self._managed_devices[x].platforms[i].keys())

        platforms = set(platforms)
        [
            self._hass.async_create_task(
                self._hass.config_entries.async_forward_entry_setup(config_entry, x)
            )
            for x in platforms
        ]

    async def async_add_entities(
        self, config_entry: ConfigEntry, entity_type: str, cls_list, async_add_entities
    ):
        """根据ConfigEntry创建Entity"""
        devices = []
        for x in self._entries_devices[config_entry.entry_id]:
            for i in range(len(self._managed_devices[x].platforms)):
                # if any one entity_type exist, append device
                if entity_type in self._managed_devices[x].platforms[i]:
                    devices.append(self._managed_devices[x])
                    break

        entities = []
        for device in devices:
            params = []
            self._devices_entities.setdefault(device.did, [])
            for aiot_device in AIOT_DEVICE_MAPPING:
                if device.model in aiot_device:
                    for p in aiot_device['params']:
                        if entity_type in p:
                            params.append(p[entity_type])
                    break

            ch_count = None
            # 这里需要处理特殊设备
            if device.model == "lumi.airrtc.vrfegl01":
                # VRF空调控制器
                resp = await self._session.async_query_resource_value(
                    device.did, ["13.1.85"]
                )
                ch_count = int(resp[0]["value"])

            for j in range(len(params)):
                if params[j].get(MK_MAPPING_PARAMS):
                    ch_count = ch_count or params[j][MK_MAPPING_PARAMS].get("ch_count")

            if ch_count:
                for i in range(ch_count):
                    for j in range(len(params)):
                        attr = params[j].get(MK_INIT_PARAMS)[MK_HASS_NAME]
                        t = cls_list.get(attr, None)
                        if t is None:
                            t = cls_list['default']
                        instance = t(
                            self._hass,
                            device,
                            params[j][MK_RESOURCES],
                            i + 1,
                            **params[j].get(MK_INIT_PARAMS) or {},
                        )
                        self._devices_entities[device.did].append(instance)
                        entities.append(instance)
            else:
                for i in range(len(params)):
                    attr = params[i].get(MK_INIT_PARAMS)[MK_HASS_NAME]
                    t = cls_list.get(attr, None)
                    if t is None:
                        t = cls_list['default']
                    instance = t(
                        self._hass,
                        device,
                        params[i][MK_RESOURCES],
                        **params[i].get(MK_INIT_PARAMS) or {},
                    )
                    self._devices_entities[device.did].append(instance)
                    entities.append(instance)
        async_add_entities(entities, update_before_add=True)

    async def async_remove_entry(self, config_entry):
        """ConfigEntry remove."""
        self._config_entries.pop(config_entry.entry_id)
        device_ids = self._entries_devices[config_entry.entry_id]
        for device_id in device_ids:
            self._managed_devices.pop(device_id)
            self._devices_entities.pop(device_id)
