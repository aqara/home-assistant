import logging
from homeassistant.components.switch import SwitchEntity

from .aiot_manager import AiotManager, AiotToggleableEntityBase
from .const import DOMAIN, HASS_DATA_AIOT_MANAGER

TYPE = "remote"

_LOGGER = logging.getLogger(__name__)

DATA_KEY = f"{TYPE}.{DOMAIN}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    await manager.async_add_entities(
        config_entry, TYPE, AiotRemoteEntity, async_add_entities
    )


class AiotRemoteEntity(AiotToggleableEntityBase, SwitchEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotToggleableEntityBase.__init__(
            self, hass, device, res_params, TYPE, channel, **kwargs
        )
