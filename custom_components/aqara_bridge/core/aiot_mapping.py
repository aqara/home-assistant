from homeassistant.components.climate import TEMP_CELSIUS
from homeassistant.components.light import (
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    SUPPORT_COLOR_TEMP,
)
from homeassistant.components.cover import (
    SUPPORT_CLOSE,
    SUPPORT_OPEN,
    SUPPORT_SET_POSITION,
    SUPPORT_STOP,
)
from homeassistant.components.climate import (
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_FAN_MODE,
)
from homeassistant.components.remote import SUPPORT_LEARN_COMMAND
from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_DOOR,
    DEVICE_CLASS_MOISTURE,
    DEVICE_CLASS_MOTION
)
from homeassistant.const import (
    # ATTR_BATTERY_LEVEL,
    # ATTR_TEMPERATURE,
    CONDUCTIVITY,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_CO2,
    ENERGY_WATT_HOUR,
    ENERGY_KILO_WATT_HOUR,
    LIGHT_LUX,
    PERCENTAGE,
    POWER_WATT,
    PRESSURE_HPA,
    TEMP_CELSIUS,
    CONCENTRATION_PARTS_PER_BILLION,
    CONCENTRATION_PARTS_PER_MILLION,
    STATE_OPEN,
    STATE_OPENING,
    # STATE_CLOSED,
    STATE_CLOSING,
    STATE_LOCKED,
    STATE_UNLOCKED
    )

try:
    from homeassistant.const import DEVICE_CLASS_GAS
except:
    DEVICE_CLASS_GAS = "gas"
try:
    from homeassistant.const import DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS
except:
    DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS = "volatile_organic_compounds"

# AiotDevice Mapping
MK_MAPPING_PARAMS = "mapping_params"
MK_INIT_PARAMS = "init_params"
MK_RESOURCES = "resources"
MK_HASS_NAME = "hass_attr_name"

AIOT_DEVICE_MAPPING = [{
    # Aqara M1S网关
    'lumi.gateway.acn01': ["Aqara", "Gateway M1S", "ZHWG15LM"],
    'params': [
        {
            "remote": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "pair",
                    "supported_features": 0
                },
                MK_RESOURCES: {
                    "pair": ("8.0.2109", "_attr_is_on"),
                }
            }
        }, {
            "light": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "light",
                    "supported_features": SUPPORT_BRIGHTNESS | SUPPORT_COLOR,
                    "color_mode": "hs",
                },
                MK_RESOURCES: {
                    "toggle": ("14.7.111", "_attr_is_on"),
                    "color": ("14.7.85", "_attr_hs_color"),
                    "brightness": ("14.7.1006", "_attr_brightness"),
                }
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "illuminance",
                    "device_class": DEVICE_CLASS_ILLUMINANCE,
                    "state_class": "measurement",
                    "unit_of_measurement": LIGHT_LUX
                },
                MK_RESOURCES: {"illumination": ("0.3.85", "_attr_native_value")},
            }
        }
    ]
},{
    'lumi.aircondition.acn05': ["Aqara", "AirCondition P3", "KTBL12LM"],
    'params': [
        {
            "remote": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "pair",
                    "supported_features": 0
                },
                MK_RESOURCES: {
                    "pair": ("8.0.2109", "_attr_is_on"),
                }
            }
        }, {
            "remote": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "ir",
                    "supported_features": SUPPORT_LEARN_COMMAND
                },
                MK_RESOURCES: {
                    "irda": ("8.0.2092", "_attr_is_on"),
                }
            }
        }
    ]
}, {
    'lumi.gateway.aqcn02': ["Aqara", "Hub E1", "ZHWG16LM"],
    'params': [
        {
            "remote": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "pair",
                    "supported_features": 0
                },
                MK_RESOURCES: {
                    "pair": ("8.0.2109", "_attr_is_on"),
                }
            }
        }
    ]
}, {
    'lumi.gateway.iragl5': ["Aqara", "Gateway M2", "ZHWG12LM"],
    'params': [
        {
            "remote": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "pair",
                    "supported_features": 0
                },
                MK_RESOURCES: {
                    "pair": ("8.0.2109", "_attr_is_on"),
                }
            }
        }, {
            "remote": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "ir",
                    "supported_features": SUPPORT_LEARN_COMMAND
                },
                MK_RESOURCES: {
                    "irda": ("8.0.2092", "_attr_is_on"),
                }
            }
        }
    ]
}, {
    'lumi.gateway.sacn01': ["Aqara", "Smart Hub H1", "QBCZWG11LM"],
    'params': [
        {
            "remote": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "pair",
                    "supported_features": 0
                },
                MK_RESOURCES: {
                    "pair": ("8.0.2109", "_attr_is_on"),
                }
            }
        }
    ]
}, {
    'lumi.camera.gwagl02': ["Aqara", "Camera Hub G2H", "ZNSXJ12LM"],
    'params': [
        {
            "remote": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "pair",
                    "supported_features": 0
                },
                MK_RESOURCES: {
                    "pair": ("8.0.2109", "_attr_is_on"),
                }
            }
        }
    ]
}, {
    'lumi.camera.gwpagl01': ["Aqara", "Camera Hub G3", "ZNSXJ13LM"],
    'params': [
        {
            "remote": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "pair",
                    "supported_features": 0
                },
                MK_RESOURCES: {
                    "pair": ("8.0.2109", "_attr_is_on"),
                }
            }
        }
    ]
}, {
    'lumi.gateway.acn004': ["Aqara", "Gateway M1S22", "ZHWG20LM"],
    'params': [
        {
            "remote": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "pair",
                    "supported_features": 0
                },
                MK_RESOURCES: {
                    "pair": ("8.0.2109", "_attr_is_on"),
                }
            }
        }, {
            "light": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "light",
                    "supported_features": SUPPORT_BRIGHTNESS | SUPPORT_COLOR,
                    "color_mode": "hs",
                },
                MK_RESOURCES: {
                    "toggle": ("14.7.111", "_attr_is_on"),
                    "color": ("14.7.85", "_attr_hs_color"),
                    "brightness": ("14.7.1006", "_attr_brightness"),
                }
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "illuminance",
                    "device_class": DEVICE_CLASS_ILLUMINANCE,
                    "state_class": "measurement",
                    "unit_of_measurement": LIGHT_LUX
                },
                MK_RESOURCES: {"illumination": ("0.3.85", "_attr_native_value")},
            }
        }
    ]
}, {
    'virtual.ir.default': ["Aqara", "Virtual IR", ""],
    'params': [
        {
            "remote": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "ir",
                    "supported_features": 0
                },
                MK_RESOURCES: {
                    "irda": ("8.0.2092", "_attr_is_on"),
                }
            }
        }
    ]
}, {
    'lumi.ctrl_neutral1': ["Aqara", "Single Wall Switch", "QBKG04LM"],
    'lumi.switch.b1lacn02': ["Aqara", "Single Wall Switch D1", "QBKG21LM"],
    'lumi.switch.b1lc04': ["Aqara", "Single Wall Switch E1", "QBKG38LM"],
    'lumi.switch.b1laus01': ["Aqara", "Single Wall Switch US", "WS-USC01"],
    'lumi.switch.l1aeu1': ["Aqara", "Single Wall Switch EU H1", "WS-EUK01"],
    'lumi.switch.l0agl1': ["Aqara", "Relay T1", "SSM-U02"],
    'lumi.switch.l0acn1': ["Aqara", "Relay T1", "DLKZMK12LM"],
    # 智能墙壁开关T1（单火单键）
    'lumi.switch.b1lacn01': ["Aqara", "Single Wall Switch T1", "QBKG17LM"],
    'lumi.switch.acn001': ["Aqara", "Single Wall Switch X1", ""],
    'lumi.switch.b1nc01': ["Aqara", "Single Wall Switch E1", "QBKG40LM"],
    'params': [
        {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "switch",
                },
                MK_RESOURCES: {
                    "toggle": ("4.1.85", "_attr_is_on"),
                    "power": ("0.12.85", "_attr_current_power_w"),
                    "energy": ("0.13.85", "_attr_today_energy_kwh"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "lqi": ("8.0.2007", "_attr_lqi")
                }
            }
        }
    ]
}, {
    'lumi.ctrl_neutral2': ["Aqara", "Double Wall Switch", "QBKG03LM"],
    'lumi.switch.b2lacn02': ["Aqara", "Double Wall Switch D1", "QBKG22LM"],
    'lumi.switch.b2lc04': ["Aqara", "Double Wall Switch E1", "QBKG39LM"],
    'lumi.switch.b2laus01': ["Aqara", "Double Wall Switch US", "WS-USC02"],
    'lumi.switch.l2aeu1': ["Aqara", "Double Wall Switch EU H1", "WS-EUK02"],
    # 智能墙壁开关T1（单火双键）
    'lumi.switch.b2lacn01': ["Aqara", "Double Wall Switch T1", "QBKG18LM"],
    'lumi.switch.acn002': ["Aqara", "Double Wall Switch X1", ""],
    'lumi.switch.b2nc01': ["Aqara", "Double Wall Switch E1", "QBKG41LM"],
    'params': [
        {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "switch",
                },
                MK_RESOURCES: {
                    "toggle": ("4.{}.85", "_attr_is_on"),
                    "power": ("0.12.85", "_attr_current_power_w"),
                    "energy": ("0.13.85", "_attr_today_energy_kwh"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "lqi": ("8.0.2007", "_attr_lqi")
                }
            }
        }
    ]
}, {
    'lumi.switch.l3acn3': ["Aqara", "Triple Wall Switch D1", "QBKG25LM"],
    # 智能墙壁开关T1（单火三键）
    'lumi.switch.acn003': ["Aqara", "Triple Wall Switch X1", ""],
    'lumi.switch.b3l01': ["Aqara", "Triple Wall Switch T1", "QBKG33LM"],
    'params': [
        {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "switch",
                },
                MK_RESOURCES: {
                    "toggle": ("4.{}.85", "_attr_is_on"),
                    "power": ("0.12.85", "_attr_current_power_w"),
                    "energy": ("0.13.85", "_attr_today_energy_kwh"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "lqi": ("8.0.2007", "_attr_lqi")
                }
            }
        }
    ]
}, {
    'lumi.ctrl_ln1': ["Aqara", "Single Wall Switch", "QBKG11LM"],
    'lumi.ctrl_ln1.aq1': ["Aqara", "Single Wall Switch", "QBKG11LM"],
    'lumi.ctrl_86plug.v1': ["Aqara", "Socket", "QBCZ11LM"],
    'lumi.ctrl_86plug.aq1': ["Aqara", "Socket", "QBCZ11LM"],
    'lumi.ctrl_86plug.es1': ["Aqara", "Socket", "QBCZ11LM"],
    'lumi.switch.b1nacn02': ["Aqara", "Single Wall Switch D1", "QBKG23LM"],
    'lumi.switch.n1acn1': ["Aqara", "Single Wall Switch H1 Pro", "QBKG30LM"],
    'lumi.switch.b1naus01': ["Aqara", "Single Wall Switch US", "WS-USC03"],
    'lumi.switch.n1aeu1': ["Aqara", "Single Wall Switch EU H1", "WS-EUK03"],
    'lumi.switch.n0agl1': ["Aqara", "Relay T1", "SSM-U01"],
    'lumi.switch.n0acn1': ["Aqara", "Relay T1", "DLKZMK11LM"],
    'lumi.switch.n0acn2': ["Aqara", "Relay T1", "DLKZMK11LM"],
    'lumi.plug.maeu01': ["Aqara", "Plug", "SP-EUC01"],
    # 智能墙壁开关T1（零火单键）
    'lumi.switch.b1nacn01': ["Aqara", "Single Wall Switch T1", "QBKG19LM"],
    'lumi.switch.acn004': ["Aqara", "Single Wall Switch X1", ""],
    'params': [
        {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "switch",
                },
                MK_RESOURCES: {
                    "toggle": ("4.1.85", "_attr_is_on"),
                    "power": ("0.12.85", "_attr_current_power_w"),
                    "energy": ("0.13.85", "_attr_today_energy_kwh"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "lqi": ("8.0.2007", "_attr_lqi")
                }
            }
        }, {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "decoupled"
                },
                MK_RESOURCES: {
                    "decoupled": ("4.11.85", "_attr_is_on")
                }
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "power",
                    "device_class": DEVICE_CLASS_POWER,
                    "state_class": "measurement",
                    "unit_of_measurement": POWER_WATT},
                MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")}
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "energy",
                    "device_class": DEVICE_CLASS_ENERGY,
                    "state_class": "total_increasing",
                    "unit_of_measurement": ENERGY_KILO_WATT_HOUR},
                MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.relay.c2acn01': ["Aqara", "Relay", "LLKZMK11LM"],
    'lumi.ctrl_ln2': ["Aqara", "Double Wall Switch", "QBKG12LM"],
    'lumi.ctrl_ln2.aq1': ["Aqara", "Double Wall Switch", "QBKG12LM"],
    'lumi.switch.b2nacn02': ["Aqara", "Double Wall Switch D1", "QBKG24LM"],
    'lumi.switch.n2acn1': ["Aqara", "Double Wall Switch H1 Pro", "QBKG31LM"],
    'lumi.switch.b2naus01': ["Aqara", "Double Wall Switch US", "WS-USC04"],
    'lumi.switch.n2aeu1': ["Aqara", "Double Wall Switch EU H1", "WS-EUK04"],
    # 智能墙壁开关T1（零火双键）
    'lumi.switch.b2nacn01': ["Aqara", "Double Wall Switch T1", "QBKG20LM"],
    'lumi.switch.acn005': ["Aqara", "Double Wall Switch X1", ""],
    'params': [
        {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "switch",
                },
                MK_RESOURCES: {
                    "toggle": ("4.{}.85", "_attr_is_on"),
                    "power": ("0.12.85", "_attr_current_power_w"),
                    "energy": ("0.13.85", "_attr_today_energy_kwh"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "lqi": ("8.0.2007", "_attr_lqi")
                }
            }
        }, {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "decoupled"
                },
                MK_RESOURCES: {
                    "decoupled": ("4.1{}.85", "_attr_is_on")
                }
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "power",
                    "device_class": DEVICE_CLASS_POWER,
                    "state_class": "measurement",
                    "unit_of_measurement": POWER_WATT},
                MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")}
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "energy",
                    "device_class": DEVICE_CLASS_ENERGY,
                    "state_class": "total_increasing",
                    "unit_of_measurement": ENERGY_KILO_WATT_HOUR},
                MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.switch.n3acn3': ["Aqara", "Triple Wall Switch D1", "QBKG26LM"],
    'lumi.switch.n3acn1': ["Aqara", "Triple Wall Switch H1 Pro", "QBKG32LM"],
    'lumi.switch.n4acn4': ["Aqara", "Scene Panel", "ZNCJMB14LM"],
    # 智能墙壁开关T1（零火三键）
    'lumi.switch.b3n01': ["Aqara", "Triple Wall Switch T1", "QBKG34LM"],
    'lumi.switch.acn006': ["Aqara", "Triple Wall Switch X1", ""],
    'params': [
        {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "switch",
                },
                MK_RESOURCES: {
                    "toggle": ("4.{}.85", "_attr_is_on"),
                    "power": ("0.12.85", "_attr_current_power_w"),
                    "energy": ("0.13.85", "_attr_today_energy_kwh"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "lqi": ("8.0.2007", "_attr_lqi")
                }
            }
        }, {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "decoupled"
                },
                MK_RESOURCES: {
                    "decoupled": ("4.1{}.85", "_attr_is_on")
                }
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "power",
                    "device_class": DEVICE_CLASS_POWER,
                    "state_class": "measurement",
                    "unit_of_measurement": POWER_WATT},
                MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")}
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "energy",
                    "device_class": DEVICE_CLASS_ENERGY,
                    "state_class": "total_increasing",
                    "unit_of_measurement": ENERGY_KILO_WATT_HOUR},
                MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
            }
        }
    ]
}, {
    # light with brightness and color temp
    'lumi.light.aqcn02': ["Aqara", "Bulb", "ZNLDP12LM"],
    'lumi.light.cwopcn02': ["Aqara", "Opple MX650", "XDD12LM"],
    'lumi.light.cwopcn03': ["Aqara", "Opple MX480", "XDD13LM"],
    'ikea.light.led1545g12': ["IKEA", "Bulb E27 980 lm", "LED1545G12"],
    'ikea.light.led1546g12': ["IKEA", "Bulb E27 950 lm", "LED1546G12"],
    'ikea.light.led1536g5': ["IKEA", "Bulb E14 400 lm", "LED1536G5"],
    'ikea.light.led1537r6': ["IKEA", "Bulb GU10 400 lm", "LED1537R6"],
    'lumi.light.cwacn1': ["Aqara", "0-10V Dimmer", "ZNTGMK12LM"],
    'lumi.light.cwjwcn01': ["Aqara", "Jiawen 0-12V Dimmer", "Z204"],
    'params': [
{
            "light": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "light",
                    "supported_features": SUPPORT_BRIGHTNESS | SUPPORT_COLOR,
                    "color_mode": "hs",
                },
                MK_RESOURCES: {
                    "toggle": ("4.1.85", "_attr_is_on"),
                    "brightness": ("14.1.85", "_attr_brightness"),
                    "color_temp": ("14.2.85", "_attr_color_temp")
                }
            }
        }
    ]
}, {
    # light with brightness and color temp
    'lumi.light.cwac02': ["Aqara", "Bulb T1", "ZNLDP13LM"],
    'params': [
{
            "light": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "light",
                    "supported_features": SUPPORT_BRIGHTNESS | SUPPORT_COLOR_TEMP,
                    "color_mode": "hs",
                },
                MK_RESOURCES: {
                    "toggle": ("4.1.85", "_attr_is_on"),
                    "brightness": ("1.7.85", "_attr_brightness"),
                    "color_temp": ("1.9.85", "_attr_color_temp")
                }
            }
        }
    ]
}, {
    'lumi.light.rgbac1': ["Aqara", "RGBW LED Controller T1", "ZNTGMK11LM"],
    'params': [
        {
            "light": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "light",
                    "supported_features": SUPPORT_BRIGHTNESS | SUPPORT_COLOR,
                    "color_mode": "hs",
                },
                MK_RESOURCES: {
                    "toggle": ("4.1.85", "_attr_is_on"),
                    "brightness": ("14.1.85", "_attr_brightness"),
                    "color_temp": ("14.2.85", "_attr_color_temp"),
                    "rgb_color": ("14.8.85", "_attr_rgb_color")
                }
            }
        }
    ]
}, {
    'lumi.dimmer.rcbac1': ["Aqara", "RGBW LED Dimmer", "ZNDDMK11LM"],
    'params': [
        {
            "light": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "light",
                    "supported_features": SUPPORT_BRIGHTNESS | SUPPORT_COLOR,
                    "color_mode": "hs",
                },
                MK_RESOURCES: {
                    "toggle": ("4.1.85", "_attr_is_on"),
                    "brightness": ("14.1.85", "_attr_brightness"),
                    "color_temp": ("14.2.85", "_attr_color_temp"),
                    "rgb_color": ("14.8.85", "_attr_rgb_color"),
                    "color": ("14.11.85", "_attr_hs_color")
                }
            }
        }
    ]
}, {
    # VRF空调控制器
    'lumi.airrtc.vrfegl01': ["Aqara", "VRF Air Conditioning", ""],
    'params': [
        {
            "climate": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "climate",
                    "supported_features": SUPPORT_TARGET_TEMPERATURE | SUPPORT_FAN_MODE,
                    "hvac_modes": ["cool", "heat", "off"],
                    "unit_of_measurement": TEMP_CELSIUS,
                    "target_temp_step": 1,
                    "fan_modes": ["low", "middle", "high"],
                    "min_temp": 16,
                    "max_temp": 30,
                },
                MK_RESOURCES: {"ac_state": ("14.{}.85", "_state_str")},
            }
        }
    ]
}, {
    'lumi.curtain.acn002': ["Aqara", "Roller Shade E1", "ZNJLBL01LM"],
    # Aqara智能窗帘电机（锂电池开合帘版）
    'lumi.curtain.hagl04': ["Aqara", "Curtain B1", "ZNCLDJ12LM"],
    'params': [
        {
            "cover": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "cover",
                    "supported_features": SUPPORT_OPEN
                    | SUPPORT_CLOSE
                    | SUPPORT_SET_POSITION
                    | SUPPORT_STOP,
                    "device_class": "curtain",
                },
                MK_RESOURCES: {
                    "curtain_state": ("14.2.85", "_attr_state"),
                    "running_state": ("14.4.85", "_attr_state"),
                    "position": ("1.1.85", "_attr_current_cover_position"),
                },
            },
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.sensor_switch': ["Xiaomi", "Button", "WXKG01LM"],
    'lumi.sensor_switch.aq2': ["Aqara", "Button", "WXKG11LM"],
    'lumi.remote.b1acn01': ["Aqara", "Button", "WXKG11LM"],
    'lumi.remote.b1acn02': ["Aqara", "Button", "WXKG12LM"],
    'lumi.sensor_switch.aq3': ["Aqara", "Shake Button", "WXKG12LM"],
    'lumi.sensor_86sw1': ["Aqara", "Single Wall Button", "WXKG03LM"],
    'lumi.remote.b186acn01': ["Aqara", "Single Wall Button", "WXKG03LM"],
    'lumi.remote.b186acn02': ["Aqara", "Single Wall Button D1", "WXKG06LM"],
    'lumi.remote.b18ac1': ["Aqara", "Single Wall Button H1", "WXKG14LM"],
    'lumi.remote.acn003': ["Aqara", "Single Wall Button E1", "WXKG16LM"],
    # 无线开关 T1（贴墙式单键）
    'lumi.remote.b186acn03': ["Aqara", "Single Wall Button T1", "WXKG03LM"],
    'params': [
        {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "action",
                    "device_class": "",
                    "state_class": "",
                    "unit_of_measurement": ""
                },
                MK_RESOURCES: {"button": ("13.1.85", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.sensor_86sw2': ["Aqara", "Double Wall Button", "WXKG02LM"],
    'lumi.remote.b286acn01': ["Aqara", "Double Wall Button", "WXKG02LM"],
    'lumi.sensor_86sw2.es1': ["Aqara", "Double Wall Button", "WXKG02LM"],
    'lumi.remote.b286acn02': ["Aqara", "Double Wall Button D1", "WXKG07LM"],
    'lumi.remote.b286opcn01': ["Aqara", "Opple Two Button", "WXCJKG11LM"],
    'lumi.remote.b486opcn01': ["Aqara", "Opple Four Button", "WXCJKG12LM"],
    'lumi.remote.b686opcn01': ["Aqara", "Opple Six Button", "WXCJKG13LM"],
    'lumi.remote.b28ac1': ["Aqara", "Double Wall Button H1", "WXKG15LM"],
    'lumi.remote.acn004': ["Aqara", "Double Wall Button E1", "WXKG17LM"],
    # 无线开关 T1（贴墙式双键）
    'lumi.remote.b286acn03': ["Aqara", "Double Wall Button T1", "WXKG04LM"],
    'params': [
        {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "action",
                    "device_class": "",
                    "state_class": "",
                    "unit_of_measurement": ""
                },
                MK_RESOURCES: {"button": ("13.{}.85", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.remote.rkba01': ["Aqara", "Smart Knob H1", "ZNXNKG02LM"],
    'params': [
        {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "action",
                    "device_class": "",
                    "state_class": "",
                    "unit_of_measurement": ""
                },
                MK_RESOURCES: {
                    "button": ("13.1.85", "_attr_native_value"),
                    "rotate_angle": ("0.24.85", "_attr_rotate_angle"),
                    "action_duration": ("0.25.85", "_attr_action_duration"),
                    "rotate_angle_w_hold": ("0.29.85", "_attr_rotate_angle_w_hold"),
                    "action_duration_w_hold": ("0.30.85", "_attr_action_duration_w_hold"),
                    "fw_ver": ("8.0.2002", "_attr_fw_ver"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                },
            }
        }
    ]
}, {
    # 高精度人体传感器
    'lumi.motion.agl04': ["Aqara", "Precision Motion Sensor", "RTCGQ13LM"],
    'params': [
        {
            "binary_sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "motion",
                    "device_class": DEVICE_CLASS_MOTION
                },
                MK_RESOURCES: {
                    "motion": ("3.1.85", "_attr_native_value"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "fw_ver": ("8.0.2002", "_attr_fw_ver"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "voltage": ("8.0.2008", "_attr_voltage")
                },

            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.plug': ["Xiaomi", "Plug", "ZNCZ02LM"],
    'lumi.plug.mitw01': ["Xiaomi", "Plug TW", "ZNCZ03LM"],
    'lumi.plug.mmeu01': ["Xiaomi", "Plug EU", "ZNCZ04LM"],
    'lumi.plug.maus01': ["Xiaomi", "Plug US", "ZNCZ12LM"],
    'params': [
        {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "switch"
                },
                MK_RESOURCES: {
                    "toggle": ("4.1.85", "_attr_is_on"),
                    "power": ("0.12.85", "_attr_current_power_w"),
                    "energy": ("0.13.85", "_attr_today_energy_kwh"),
                    "fw_ver": ("8.0.2002", "_attr_fw_ver"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "in_use": ("8.0.2044", "_attr_in_use")
                }
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "power",
                    "device_class": DEVICE_CLASS_POWER,
                    "state_class": "measurement",
                    "unit_of_measurement": POWER_WATT},
                MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")}
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "energy",
                    "device_class": DEVICE_CLASS_ENERGY,
                    "state_class": "total_increasing",
                    "unit_of_measurement": ENERGY_KILO_WATT_HOUR},
                MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.sensor_motion.v2': ["Xiaomi", "Motion Sensor", "RTCGQ01LM"],
    'lumi.motion.agl04': ["Aqara", "Precision Motion Sensor", "RTCGQ13LM"],
    'params': [
        {
            "binary_sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "motion",
                    "device_class": DEVICE_CLASS_MOTION
                },
                MK_RESOURCES: {
                    "motion": ("3.1.85", "_attr_native_value"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "fw_ver": ("8.0.2002", "_attr_fw_ver"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "voltage": ("8.0.2008", "_attr_voltage")
                },

            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.motion.agl02': ["Aqara", "Motion Sensor T1", "RTCGQ12LM"],
    'params': [
        {
            "binary_sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "motion",
                    "device_class": DEVICE_CLASS_MOTION
                },
                MK_RESOURCES: {
                    "motion": ("3.1.85", "_attr_native_value"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "fw_ver": ("8.0.2002", "_attr_fw_ver"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "voltage": ("8.0.2008", "_attr_voltage")
                },

            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            },
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "illuminance",
                    "device_class": DEVICE_CLASS_ILLUMINANCE,
                    "state_class": "measurement"
                },
                MK_RESOURCES: {"illuminance": ("0.3.85", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.sensor_magnet': ["Xiaomi", "Door Sensor", "MCCGQ01LM"],
    'lumi.sensor_magnet.aq2': ["Aqara", "Door Sensor", "MCCGQ11LM"],
    'lumi.magnet.agl02': ["Aqara", "Door Sensor T1", "MCCGQ12LM"],
    'lumi.magnet.acn001': ["Aqara", "Door Sensor E1", "MCCGQ14LM"],
    'lumi.magnet.ac01': ["Aqara", "Door Sensor P1", "MCCGQ13LM"],
    'params': [
        {
            "binary_sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "contact",
                    "device_class": DEVICE_CLASS_DOOR
                },
                MK_RESOURCES: {
                    "status": ("3.1.85", "_attr_native_value"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "fw_ver": ("8.0.2002", "_attr_fw_ver"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "voltage": ("8.0.2008", "_attr_voltage")
                },
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }
    ]
}, {
    # motion sensor with illuminance
    'lumi.sensor_motion.aq2': ["Aqara", "Motion Sensor", "RTCGQ11LM"],
    'params': [
        {
            "binary_sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "motion",
                    "device_class": DEVICE_CLASS_MOTION
                },
                MK_RESOURCES: {
                    "motion": ("3.1.85", "_attr_native_value"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "fw_ver": ("8.0.2002", "_attr_fw_ver"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "voltage": ("8.0.2008", "_attr_voltage")
                },

            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }
    ]
}, {
    # temperature and humidity sensor
    'lumi.sensor_ht': ["Xiaomi", "TH Sensor", "WSDCGQ01LM"],
    'params': [
        {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "temperature",
                    "device_class": DEVICE_CLASS_TEMPERATURE,
                    "state_class": "measurement",
                    "unit_of_measurement": TEMP_CELSIUS
                },
                MK_RESOURCES: {"temperature": ("'0.1.85", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "humidity",
                    "device_class": DEVICE_CLASS_HUMIDITY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"humidity": ("0.2.85", "_attr_native_value")},
            }
        }
    ]
}, {
    # temperature, humidity and pressure sensor
    'lumi.weather': ["Aqara", "TH Sensor", "WSDCGQ11LM"],
    'lumi.sensor_ht.agl02': ["Aqara", "TH Sensor", "WSDCGQ12LM"],
    'params': [
        {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "temperature",
                    "device_class": DEVICE_CLASS_TEMPERATURE,
                    "state_class": "measurement",
                    "unit_of_measurement": TEMP_CELSIUS
                },
                MK_RESOURCES: {"temperature": ("'0.1.85", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "humidity",
                    "device_class": DEVICE_CLASS_HUMIDITY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"humidity": ("0.2.85", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "pressure",
                    "device_class": DEVICE_CLASS_PRESSURE,
                    "state_class": "measurement",
                    "unit_of_measurement": PRESSURE_HPA
                },
                MK_RESOURCES: {"pressure": ("0.3.85", "_attr_native_value")},
            }
        }
    ]
}, {
    # water leak sensor
    'lumi.sensor_wleak.aq1': ["Aqara", "Water Leak Sensor", "SJCGQ11LM"],
    'lumi.flood.agl02': ["Aqara", "Water Leak Sensor T1", "SJCGQ12LM"],
    'lumi.flood.acn001': ["Aqara", "Water Leak Sensor E1", "SJCGQ13LM"],
    'params': [
        {
            "binary_sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "moisture",
                    "device_class": DEVICE_CLASS_MOISTURE
                },
                MK_RESOURCES: {
                    "moisture": ("3.1.85", "_attr_native_value"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "fw_ver": ("8.0.2002", "_attr_fw_ver"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "voltage": ("8.0.2008", "_attr_voltage")
                },
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.sen_ill.agl01': ["Aqara", "Light Sensor T1", "GZCGQ11LM"],
    'lumi.sen_ill.mgl01': ["Xiaomi", "Light Sensor", "GZCGQ01LM"],
    'params': [
        {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "illuminance",
                    "device_class": DEVICE_CLASS_ILLUMINANCE,
                    "state_class": "measurement",
                    "unit_of_measurement": LIGHT_LUX
                },
                MK_RESOURCES: {"illumination": ("0.3.85", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.sensor_smoke': ["Honeywell", "Smoke Sensor", "JTYJ-GD-01LM/BW"],
    'params': [
        {
            "binary_sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "smoke"
                },
                MK_RESOURCES: {
                    "smoke": ("13.1.85", "_attr_native_value"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "fw_ver": ("8.0.2002", "_attr_fw_ver"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "voltage": ("8.0.2008", "_attr_voltage")
                },
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "smoke_density",
                    "device_class": "smoke",
                    "state_class": "measurement",
                    "unit_of_measurement": CONCENTRATION_PARTS_PER_MILLION
                },
                MK_RESOURCES: {"smoke": ("0.1.85", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.sensor_natgas': ["Honeywell", "Gas Sensor", "JTQJ-BF-01LM/BW"],
    'params': [
        {
            "binary_sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "natgas"
                },
                MK_RESOURCES: {
                    "gas": ("13.1.85", "_attr_native_value"),
                    "chip_temperature": ("8.0.2006", "_attr_chip_temperature"),
                    "fw_ver": ("8.0.2002", "_attr_fw_ver"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "voltage": ("8.0.2008", "_attr_voltage")
                },
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "natgas",
                    "device_class": DEVICE_CLASS_GAS,
                    "state_class": "measurement",
                    "unit_of_measurement": CONCENTRATION_PARTS_PER_MILLION
                },
                MK_RESOURCES: {"gas": ("0.1.85", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.airmonitor.acn01': ["Aqara", "Smart TVOC Air Quality Monitor", "VOCKQJK11LM"],
    'params': [
        {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("8.0.2001", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "temperature",
                    "device_class": DEVICE_CLASS_TEMPERATURE,
                    "state_class": "measurement",
                    "unit_of_measurement": TEMP_CELSIUS
                },
                MK_RESOURCES: {"temperature": ("'0.1.85", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "humidity",
                    "device_class": DEVICE_CLASS_HUMIDITY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"humidity": ("0.2.85", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "tvoc",
                    "device_class": DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS,
                    "state_class": "measurement",
                    "unit_of_measurement": ''
                },
                MK_RESOURCES: {"tvoc": ("0.3.85", "_attr_native_value")},
            }
        }, {
            "air_quality": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "tvoc_level",
                    "device_class": '',
                    "state_class": "measurement",
                    "unit_of_measurement": ''
                },
                MK_RESOURCES: {"tvoc_level": ("13.1.85", "_attr_tvoc_level")},
            }
        }
    ]
}, {
    'aqara.lock.bzacn3': ["Aqara", "Door Lock N100", "ZNMS16LM"],
    'aqara.lock.bzacn4': ["Aqara", "Door Lock N100", "ZNMS16LM"],
    'params': [
        {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("13.56.85", "_attr_native_value")},
            }
        }
    ]
}, {
    'aqara.lock.wbzac1': ["Aqara", "Door Lock P100", "ZNMS19LM"],
    'params': [
        {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "li_battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"li_battery": ("13.32.85", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "battery",
                    "device_class": DEVICE_CLASS_BATTERY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"battery": ("13.37.85", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "lock",
                    "device_class": "",
                    "state_class": "",
                    "unit_of_measurement": ""
                },
                MK_RESOURCES: {"lock_state": ("13.17.85", "_attr_native_value")},
            }
        }
    ]
}]

SPECIAL_DEVICES_INFO = {
    # VRF空调控制器
    "lumi.airrtc.vrfegl01": {
        "toggle": {0: "on", 1: "off"},
        "hvac_mode": {
            0: "heat",
            1: "cool",
            2: "auto",
            3: "dry",
            4: "fan_only",
        },
        "fan_mode": {0: "low", 1: "middle", 2: "high", 3: "auto"},
        "swing_mode": {0: "horizontal", 1: "vertical", 2: "both"},
        "swing_toggle": {1: "off"},
    }
}
