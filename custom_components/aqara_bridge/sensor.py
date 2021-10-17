import time
from homeassistant.components.sensor import SensorEntity

from .core.aiot_manager import (
    AiotManager,
    AiotEntityBase,
)
from .core.const import (
    BUTTON,
    BUTTON_BOTH,
    CUBE,
    DOMAIN,
    HASS_DATA_AIOT_MANAGER,
    PROP_TO_ATTR_BASE,
    VIBRATION
)

TYPE = "sensor"

DATA_KEY = f"{TYPE}.{DOMAIN}"

ATTR_ROTATE_ANGLE = "rotate_angle"
ATTR_ACTION_DURATION = "action_duration"
ATTR_ROTATE_ANGLE_W_HOLD = "rotate_angle_w_hold"
ATTR_ACTION_DURATION_W_HOLD = "action_duration_w_hold"

PROP_TO_ATTR = {
    "rotate_angle": ATTR_ROTATE_ANGLE,
    "action_duration": ATTR_ACTION_DURATION,
    "rotate_angle_w_hold": ATTR_ROTATE_ANGLE_W_HOLD,
    "action_duration_w_hold": ATTR_ACTION_DURATION_W_HOLD
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {
        "action": AiotActionSensor,
        "default": AiotSensorEntity
    }
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotSensorEntity(AiotEntityBase, SensorEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_state_class = kwargs.get("state_class")
        self._attr_name = f"{self._attr_name} {self._attr_device_class}"

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "battry":
            return int(res_value)
        if res_name == "energy":
            return round(float(res_value) / 1000.0, 3)
        return super().convert_res_to_attr(res_name, res_value)


class AiotActionSensor(AiotSensorEntity, SensorEntity):
    @property
    def icon(self):
        return 'mdi:bell'

    @property
    def rotate_angle(self):
        """Return the rotate angle."""
        return self._attr_rotate_angle

    @property
    def action_duration(self):
        """Return the action duration."""
        return self._attr_action_duration

    @property
    def rotate_angle_w_hold(self):
        """Return the rotate angle with hold"""
        return self._attr_rotate_angle_w_hold

    @property
    def action_duration_w_hold(self):
        """Return the action duration with hold."""
        return self._attr_action_duration_w_hold

    @property
    def extra_state_attributes(self):
        """Return the optional state attributes."""
        data = {}

        for prop, attr in PROP_TO_ATTR_BASE.items():
            value = getattr(self, prop)
            if value is not None:
                data[attr] = value

        for prop, attr in PROP_TO_ATTR.items():
            value = getattr(self, prop)
            if value is not None:
                data[attr] = value

        return data

    def convert_res_to_attr(self, res_name, res_value):

        if res_name == "chip_temperature":
            return round(float(res_value), 1)
        if res_name == "fw_ver":
            return res_value
        if res_name == "lqi":
            return int(res_value)
        if res_name == "rotate_angle":
            return res_value
        if res_name == "action_duration":
            return res_value
        if res_name == "rotate_angle_w_hold":
            return res_value
        if res_name == "action_duration_w_hold":
            return res_value
        if res_value != 0 and res_value != "" and res_name == "button":
            if res_name == 'vibration' and res_value != '2':
                click_type = VIBRATION.get(res_value, 'unkown')
            if "button" in res_name:
                click_type = BUTTON.get(res_value, 'unkown')
            if "cube" in res_name:
                click_type = CUBE.get(res_value, 'unkown')

            # repeat event from Aqara integration
            self.hass.bus.fire('xiaomi_aqara.click', {
                'entity_id': self.entity_id, 'click_type': click_type
            })

            time.sleep(.3)

            self.schedule_update_ha_state()
            return click_type
        return super().convert_res_to_attr(res_name, res_value)