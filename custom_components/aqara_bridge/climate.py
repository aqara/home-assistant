import logging
from homeassistant.components.climate import ClimateEntity

from .core.aiot_manager import (
    AiotManager,
    AiotEntityBase,
)
from .core.aiot_mapping import SPECIAL_DEVICES_INFO
from .core.const import DOMAIN, HASS_DATA_AIOT_MANAGER

TYPE = "climate"

_LOGGER = logging.getLogger(__name__)

DATA_KEY = f"{TYPE}.{DOMAIN}"


AC_STATE_MAPPING = {
    "hvac_mode": {
        "off": [{"code": "0000", "start": 0, "end": 4}],
        "heat": [
            {"code": "0001", "start": 0, "end": 4},
            {"code": "0000", "start": 4, "end": 8},
        ],
        "cool": [
            {"code": "0001", "start": 0, "end": 4},
            {"code": "0001", "start": 4, "end": 8},
        ],
    },
    "fan_mode": {
        "low": [{"code": "0000", "start": 8, "end": 12}],
        "middle": [{"code": "0001", "start": 8, "end": 12}],
        "high": [{"code": "0010", "start": 8, "end": 12}],
    },
    "temperature": {"0": [{"start": 16, "end": 24}]},
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {
        "default": AiotClimateEntity
    }
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotClimateEntity(AiotEntityBase, ClimateEntity):
    """VRF空调控制器，特殊资源定义，https://opendoc.aqara.cn/docs/%E4%BA%91%E5%AF%B9%E6%8E%A5%E5%BC%80%E5%8F%91%E6%89%8B%E5%86%8C/%E9%99%84%E5%BD%95/%E7%89%B9%E6%AE%8A%E8%B5%84%E6%BA%90%E5%AE%9A%E4%B9%89.html"""

    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_hvac_modes = kwargs.get("hvac_modes")
        self._attr_temperature_unit = kwargs.get("unit_of_measurement")
        self._attr_target_temperature_step = kwargs.get("target_temp_step")
        self._attr_fan_modes = kwargs.get("fan_modes")
        self._attr_min_temp = kwargs.get("min_temp")
        self._attr_max_temp = kwargs.get("max_temp")
        self._state_str = "".zfill(32)

    async def _async_change_ac_state(self, attr_name, attr_value, fix_code=None):
        mappings = AC_STATE_MAPPING[attr_name].get(attr_value)
        new_state_str = self._state_str
        if mappings:
            for mapping in mappings:
                code = fix_code if fix_code else mapping["code"]
                start = mapping["start"]
                end = mapping["end"]
                new_state_str = f"{new_state_str[0:start]}{code}{new_state_str[end:]}"

            await self.async_set_resource("ac_state", new_state_str)
        else:
            _LOGGER.warn(f"Attr value '{attr_value}' is not supported in {attr_name}")

    async def async_set_fan_mode(self, fan_mode: str):
        await self._async_change_ac_state("fan_mode", fan_mode)

    async def async_set_hvac_mode(self, hvac_mode: str):
        await self._async_change_ac_state("hvac_mode", hvac_mode)

    async def async_set_temperature(self, **kwargs):
        temperature = kwargs.get("temperature")
        await self._async_change_ac_state(
            "temperature", "0", bin(int(temperature))[2:].zfill(8)
        )

    def convert_attr_to_res(self, res_name, value):
        if res_name == "ac_state":
            # res_value：二进制字符串
            return int(value, 2)
        return super().convert_attr_to_res(res_name, value)

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "ac_state":
            # res_value: 十进制字符串
            return bin(int(res_value))[2:].zfill(32)
        return super().convert_res_to_attr(res_name, res_value)

    def __setattr__(self, name: str, value):
        if name == "_state_str" and value != "".zfill(32):
            sdi = SPECIAL_DEVICES_INFO[self._device.model]
            self._attr_hvac_mode = sdi["hvac_mode"][int(value[4:8], 2)]
            if int(value[0:4], 2) == 0:
                self._attr_hvac_mode = "off"
            self._attr_fan_mode = sdi["fan_mode"][int(value[8:12], 2)]
            self._attr_target_temperature = int(value[16:24], 2)
        return super().__setattr__(name, value)
