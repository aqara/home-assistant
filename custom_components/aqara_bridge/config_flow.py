import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries

from . import init_hass_data, data_masking, gen_auth_entry
from .const import (
    DOMAIN,
    CONF_FIELD_ACCOUNT,
    CONF_FIELD_COUNTRY_CODE,
    CONF_FIELD_AUTH_CODE,
    CONF_FIELD_SELECTED_DEVICES,
    CONF_FIELD_REFRESH_TOKEN,
    CONF_ENTRY_AUTH_ACCOUNT,
    HASS_DATA_AIOTCLOUD,
    HASS_DATA_AIOT_MANAGER,
    SERVER_COUNTRY_CODES,
    SERVER_COUNTRY_CODES_DEFAULT,
    CONF_ENTRY_AUTH_ACCOUNT,
    HASS_DATA_AUTH_ENTRY_ID,
)

_LOGGER = logging.getLogger(__name__)

DEVICE_GET_AUTH_CODE_CONFIG = vol.Schema(
    {
        vol.Required(CONF_FIELD_ACCOUNT): str,
        vol.Required(
            CONF_FIELD_COUNTRY_CODE, default=SERVER_COUNTRY_CODES_DEFAULT
        ): vol.In(SERVER_COUNTRY_CODES),
        vol.Optional(CONF_FIELD_REFRESH_TOKEN): str,
    }
)

DEVICE_GET_TOKEN_CONFIG = vol.Schema({vol.Required(CONF_FIELD_AUTH_CODE): str})


class AqaraBridgeFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle an Aqara Bridge config flow."""

    VERSION = 1

    def __init__(self):
        """Initialize."""
        self.account = None
        self.country_code = None
        self.account_type = None
        self._session = None
        self._device_manager = None

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        init_hass_data(self.hass)
        self._device_manager = self.hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
        auth_entry_id = self.hass.data[DOMAIN][HASS_DATA_AUTH_ENTRY_ID]
        self._session = self.hass.data[DOMAIN][HASS_DATA_AIOTCLOUD]
        if auth_entry_id:
            return await self.async_step_select_devices()
        else:
            # self._session = AiotCloud(
            #     aiohttp_client.async_create_clientsession(self.hass)
            # )
            # self.hass.data[DOMAIN][HASS_DATA_AIOTCLOUD] = self._session
            return await self.async_step_get_auth_code()

    async def async_step_get_auth_code(self, user_input=None):
        """Configure an aqara device through the Aqara Cloud."""
        errors = {}
        if user_input:
            self.account = user_input.get(CONF_FIELD_ACCOUNT)
            self.country_code = user_input.get(CONF_FIELD_COUNTRY_CODE)
            self.account_type = 0
            self._session.set_country(self.country_code)

            refresh_token = user_input.get(CONF_FIELD_REFRESH_TOKEN)
            if refresh_token and refresh_token != "":
                resp = await self._session.async_refresh_token(refresh_token)
                if resp["code"] == 0:
                    auth_entry = gen_auth_entry(
                        self.account,
                        self.account_type,
                        self.country_code,
                        resp["result"],
                    )
                    self.hass.async_add_job(
                        self.hass.config_entries.flow.async_init(
                            DOMAIN, context={"source": "get_token"}, data=auth_entry
                        )
                    )
                    return await self.async_step_select_devices()
                else:
                    # TODO 这里要处理API失败的情况
                    pass
            else:
                resp = await self._session.async_get_auth_code(self.account, 0)
                if resp["code"] == 0:
                    return await self.async_step_get_token()
                else:
                    # TODO 这里要处理API失败的情况
                    pass

        return self.async_show_form(
            step_id="get_auth_code",
            data_schema=DEVICE_GET_AUTH_CODE_CONFIG,
            errors=errors,
        )

    async def async_step_get_token(self, user_input=None):
        errors = {}
        if user_input:
            if CONF_FIELD_AUTH_CODE in user_input:
                auth_code = user_input.get(CONF_FIELD_AUTH_CODE)
                resp = await self._session.async_get_token(auth_code, self.account, 0)

                if resp["code"] == 0:
                    auth_entry = gen_auth_entry(
                        self.account,
                        self.account_type,
                        self.country_code,
                        resp["result"],
                    )
                    self.hass.async_add_job(
                        self.hass.config_entries.flow.async_init(
                            DOMAIN, context={"source": "get_token"}, data=auth_entry
                        )
                    )
                else:
                    errors["base"] = "cloud_credentials_incomplete"
            elif CONF_ENTRY_AUTH_ACCOUNT in user_input:
                return self.async_create_entry(
                    title=data_masking(user_input[CONF_ENTRY_AUTH_ACCOUNT], 4),
                    data=user_input,
                )

            return await self.async_step_select_devices()

        return self.async_show_form(
            step_id="get_token", data_schema=DEVICE_GET_TOKEN_CONFIG, errors=errors
        )

    async def async_step_select_devices(self, user_input=None):
        errors = {}
        if user_input:
            if CONF_FIELD_SELECTED_DEVICES in user_input:
                dids = user_input[CONF_FIELD_SELECTED_DEVICES]
                devices = await self._session.async_query_device_info(dids)
                for device in devices:
                    self.hass.async_add_job(
                        self.hass.config_entries.flow.async_init(
                            DOMAIN, context={"source": "select_devices"}, data=device
                        )
                    )
            elif "did" in user_input:
                await self.async_set_unique_id(
                    user_input["did"], raise_on_progress=False
                )
                return self.async_create_entry(
                    title=user_input["deviceName"], data=user_input
                )

            return self.async_abort(reason="complete")

        devlist = {}
        await self._device_manager.async_refresh_all_devices()  # 刷新一下
        [
            devlist.setdefault(x.did, f"{x.device_name} - {x.model}")
            for x in self._device_manager.unmanaged_gateways
        ]
        return self.async_show_form(
            step_id="select_devices",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_FIELD_SELECTED_DEVICES, default=[]
                    ): cv.multi_select(devlist)
                }
            ),
            errors=errors,
        )
