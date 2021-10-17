""" Aqara Bridge remote """
import asyncio
import time
import voluptuous as vol

from homeassistant.helpers import config_validation as cv
from homeassistant.components.remote import (
    ATTR_DELAY_SECS,
    ATTR_NUM_REPEATS,
    DEFAULT_DELAY_SECS,
    RemoteEntity
)
from homeassistant.const import CONF_TIMEOUT

from .core.aiot_manager import AiotManager, AiotEntityBase
from .core.const import DOMAIN, HASS_DATA_AIOT_MANAGER

TYPE = "remote"

DATA_KEY = f"{TYPE}.{DOMAIN}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {
        "pair": AiotRemotePair,
        "ir": AiotRemoteIrda,
        "default": AiotRemoteEntity
    }
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotRemoteEntity(AiotEntityBase, RemoteEntity):
    def __init__(self, hass, device, res_params, **kwargs):
        AiotEntityBase.__init__(
            self, hass, device, res_params, TYPE, **kwargs
        )
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs):
        await self.async_set_resource("remote", True)

    async def async_turn_off(self, **kwargs):
        await self.async_set_resource("remote", False)

    def convert_attr_to_res(self, res_name, attr_value):
        return super().convert_attr_to_res(res_name, attr_value)

    def convert_res_to_attr(self, res_name, res_value):
        return super().convert_res_to_attr(res_name, res_value)


class AiotRemotePair(AiotEntityBase, RemoteEntity):
    def __init__(self, hass, device, res_params, **kwargs):
        AiotEntityBase.__init__(
            self, hass, device, res_params, TYPE, **kwargs
        )
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs):
        await self.async_device_connection(True)

    async def async_turn_off(self, **kwargs):
        await self.async_device_connection(False)


class AiotRemoteIrda(AiotEntityBase, RemoteEntity):
    def __init__(self, hass, device, res_params, **kwargs):
        AiotEntityBase.__init__(
            self, hass, device, res_params, TYPE, **kwargs
        )
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs):
        """Turn the remote on."""

    async def async_turn_off(self, **kwargs):
        """Turn the remote off."""

    async def async_send_command(self, command, **kwargs):
        """ send command """
        num_repeats = kwargs.get(ATTR_NUM_REPEATS, 1)
        delay = kwargs.get(ATTR_DELAY_SECS, DEFAULT_DELAY_SECS)

        for _ in range(num_repeats):
            await self.async_set_resource("irda", command)
            time.sleep(delay)

    async def async_learn_command(self, **kwargs):
        """Handle a learn command."""
        timeout = kwargs.get(CONF_TIMEOUT, 10)

        resp = await self.async_infrared_learn(True, 20)
        if isinstance(resp, dict):
            keyid = resp['keyId']

            start_time = utcnow()
            while (utcnow() - start_time) < timedelta(seconds=timeout):
                message = await self.hass.async_add_executor_job(
                    self.async_received_learnresult, keyid)
                self.debug("Message received from device: '%s'", message)

                if isinstance(message, dict):
                    log_msg = "Received command is: {}".format(message['ircode'])
                    self.hass.components.persistent_notification.async_create(
                        log_msg, title="Aqara Remote"
                    )
                    return

                if message is None:
                    await self.async_infrared_learn(False)

                await asyncio.sleep(1)
