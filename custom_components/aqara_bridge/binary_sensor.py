"""Support for Xiaomi Aqara binary sensors."""
import time

from homeassistant.config import DATA_CUSTOMIZE
from homeassistant.helpers.event import async_call_later
from homeassistant.components.binary_sensor import BinarySensorEntity

from .core.aiot_manager import (
    AiotManager,
    AiotEntityBase,
)
from .core.const import (
    CONF_OCCUPANCY_TIMEOUT,
    DOMAIN,
    HASS_DATA_AIOT_MANAGER,
    PROP_TO_ATTR_BASE
)

TYPE = "binary_sensor"

DATA_KEY = f"{TYPE}.{DOMAIN}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {
        "motion": AiotMotionBinarySensor,
        "contact": AiotDoorBinarySensor,
        "default": AiotBinarySensorEntity
    }
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotBinarySensorEntity(AiotEntityBase, BinarySensorEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_state_class = kwargs.get("state_class")
        self._attr_name = f"{self._attr_name} {self._attr_device_class}"

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "chip_temperature":
            return round(float(res_value), 1)
        if res_name == "fw_ver":
            return res_value
        if res_name == "lqi":
            return int(res_value)
        if res_name == "voltage":
            return format(float(res_value) / 1000, '.3f')
        return super().convert_res_to_attr(res_name, res_value)

    @property
    def extra_state_attributes(self):
        """Return the optional state attributes."""
        data = {}

        for prop, attr in PROP_TO_ATTR_BASE.items():
            value = getattr(self, prop)
            if value is not None:
                data[attr] = value

        return data

class AiotMotionBinarySensor(AiotBinarySensorEntity, BinarySensorEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_state_class = kwargs.get("state_class")
        self._attr_name = f"{self._attr_name} {self._attr_device_class}"
        self._default_delay = 120
        self._last_on = 0
        self._last_off = 0
        self._timeout_pos = 0
        self._unsub_set_no_motion = None
        self._attr_is_on = False

    async def _start_no_motion_timer(self, delay: float):
        if self._unsub_set_no_motion:
            self._unsub_set_no_motion()

        self._unsub_set_no_motion = async_call_later(
            self.hass, abs(delay), self._set_no_motion)

    async def _set_no_motion(self, *args):
        self._last_off = time.time()
        self._timeout_pos = 0
        self._unsub_set_no_motion = None
        self._attr_is_on = False
        self.schedule_update_ha_state()

        # repeat event from Aqara integration
        self.hass.bus.fire('xiaomi_aqara.motion', {
            'entity_id': self.entity_id
        })

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "chip_temperature":
            return format((int(res_value) - 32) * 5 / 9, '.2f')
        if res_name == "fw_ver":
            return res_value
        if res_name == "lqi":
            return int(res_value)
        if res_name == "voltage":
            return format(float(res_value) / 1000, '.3f')

        time_now = time.time()

        if time_now - self._last_on < 1:
            return
        self._attr_is_on = bool(res_value)
        self._last_on = time_now

        # handle available change
        self.schedule_update_ha_state()

        if self._unsub_set_no_motion:
            self._unsub_set_no_motion()

        custom = self.hass.data[DATA_CUSTOMIZE].get(self.entity_id)
        # if customize of any entity will be changed from GUI - default value
        # for all motion sensors will be erased
        timeout = custom.get(CONF_OCCUPANCY_TIMEOUT, self._default_delay)
        if timeout:
            if isinstance(timeout, list):
                pos = min(self._timeout_pos, len(timeout) - 1)
                delay = timeout[pos]
                self._timeout_pos += 1
            else:
                delay = timeout

            if delay < 0 and time_now + delay < self._last_off:
                delay *= 2
            self.hass.add_job(self._start_no_motion_timer, delay)

        # repeat event from Aqara integration
        self.hass.bus.fire('xiaomi_aqara.motion', {
            'entity_id': self.entity_id
        })
        return bool(res_value)


class AiotDoorBinarySensor(AiotBinarySensorEntity, BinarySensorEntity):
    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "chip_temperature":
            return round(float(res_value), 1)
        if res_name == "fw_ver":
            return res_value
        if res_name == "lqi":
            return int(res_value)
        if res_name == "voltage":
            return format(float(res_value) / 1000, '.3f')

        self._attr_is_on = not bool(res_value)
        self.schedule_update_ha_state()
        return not bool(res_value)
