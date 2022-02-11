"""Support for Aqara Air Quality Monitor."""
from homeassistant.components.air_quality import AirQualityEntity
from homeassistant.const import (
    ATTR_TEMPERATURE
)

from .core.aiot_manager import (
    AiotManager,
    AiotEntityBase,
)
from .core.const import (
    ATTR_CO2E,
    ATTR_HUMIDITY,
    ATTR_TVOC,
    DOMAIN,
    HASS_DATA_AIOT_MANAGER,
    PROP_TO_ATTR_BASE
)

TYPE = "air_quality"

DATA_KEY = f"{TYPE}.{DOMAIN}"

PROP_TO_ATTR = {
    "temperature": ATTR_TEMPERATURE,
    "humidity": ATTR_HUMIDITY
}

PROP_TO_ATTR_TVOC = {
    "tvoc_level": ATTR_TVOC,
}

PROP_TO_ATTR_CO2E = {
    "carbon_dioxide_equivalent": ATTR_CO2E,
}

async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {
        "tvoc_level": AiotTvocEntity,
        "default": AiotAirMonitorEntity
    }
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotAirMonitorEntity(AiotEntityBase, AirQualityEntity):
    """ Air Monitor Entity"""
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_state_class = kwargs.get("state_class")
        self._attr_name = f"{self._attr_name} {self._attr_device_class}"
        self._attr_temperature = None
        self._attr_humidity = None
        self._attr_particulate_matter_2_5 = None
        self._attr_particulate_matter_0_1 = None
        self._attr_particulate_matter_1_0 = None

    @property
    def carbon_dioxide_equivalent(self):
        """Return the CO2e (carbon dioxide equivalent) level."""
        return self._attr_carbon_dioxide_equivalent

    @property
    def temperature(self):
        """Return the current temperature."""
        return self._attr_temperature

    @property
    def humidity(self):
        """Return the current humidity."""
        return self._attr_humidity

    @property
    def particulate_matter_0_1(self):
        """Return the particulate matter 0.1 level."""
        return self._attr_particulate_matter_0_1

    @property
    def particulate_matter_2_5(self):
        """Return the particulate matter 2.5 level."""
        return self._attr_particulate_matter_2_5

    @property
    def particulate_matter_10(self):
        """Return the particulate matter 10 level."""
        return self._attr_particulate_matter_1_0

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "chip_temperature":
            return round(float(res_value), 1)
        if res_name == "fw_ver":
            return res_value
        if res_name == "lqi":
            return int(res_value)
        if res_name == "voltage":
            return format(float(res_value) / 1000, '.3f')
        if res_name == "co2e":
            return round(float(res_value), 1)
        if res_name == "temperature":
            return round(float(res_value), 1)
        if res_name == "humidity":
            return round(float(res_value / 100), 1) 
        return super().convert_res_to_attr(res_name, res_value)

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


class AiotTvocEntity(AiotAirMonitorEntity, AirQualityEntity):
    """Air Quality class for Aqara TVOC device."""
    _attr_tvoc_level = None

    @property
    def tvoc_level(self):
        """Return the total volatile organic compounds."""
        return self._attr_tvoc_level

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

        for prop, attr in PROP_TO_ATTR_TVOC.items():
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
        if res_name == "voltage":
            return format(float(res_value) / 1000, '.3f')
        if res_name == "tvoc_level":
            return int(res_value)
        if res_name == "temperature":
            return round(float(res_value), 1)
        if res_name == "humidity":
            return round(float(res_value), 1)
        return super().convert_res_to_attr(res_name, res_value)

