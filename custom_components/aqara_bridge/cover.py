import logging
from homeassistant.components.cover import CoverEntity

from .core.aiot_manager import (
    AiotManager,
    AiotEntityBase,
)
from .core.const import DOMAIN, HASS_DATA_AIOT_MANAGER

TYPE = "cover"

_LOGGER = logging.getLogger(__name__)

DATA_KEY = f"{TYPE}.{DOMAIN}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {
        "default": AiotCoverEntity
    }
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotCoverEntity(AiotEntityBase, CoverEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_is_closed = None

    async def async_open_cover(self, **kwargs):
        return await super().async_open_cover(**kwargs)

    async def async_close_cover(self, **kwargs):
        return await super().async_close_cover(**kwargs)

    async def async_set_cover_position(self, **kwargs):
        return await super().async_set_cover_position(**kwargs)

    async def async_stop_cover(self, **kwargs):
        return await super().async_stop_cover(**kwargs)

    async def async_open_cover_tilt(self, **kwargs):
        return await super().async_open_cover_tilt(**kwargs)

    async def async_close_cover_tilt(self, **kwargs):
        return await super().async_close_cover_tilt(**kwargs)

    async def async_set_cover_tilt_position(self, **kwargs):
        return await super().async_set_cover_tilt_position(**kwargs)

    async def async_stop_cover_tilt(self, **kwargs):
        return await super().async_stop_cover_tilt(**kwargs)

    def convert_attr_to_res(self, res_name, attr_value):
        if res_name == "curtain_state":
            print(attr_value)
        elif res_name == "position":
            return str(attr_value)
        return super().convert_attr_to_res(res_name, attr_value)

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "curtain_state":
            print(res_value)
        elif res_name == "position":
            return int(res_value)
        return super().convert_res_to_attr(res_name, res_value)

    def __setattr__(self, name: str, value):
        if name == "_attr_state":
            print(value)
        return super().__setattr__(name, value)
