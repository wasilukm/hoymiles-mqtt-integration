"""Integration common constants."""

from typing import Any, NamedTuple

import voluptuous as vol
from homeassistant.helpers.selector import Selector, selector

NAME = "MQTT Hoymiles"
DOMAIN = "mqtt_hoymiles"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.0"

ISSUE_URL = "https://github.com/wasilukm/hoymiles-mqtt-integration/issues"

NO_CONFIG_VALUE = "NO_VALUE"


class ConfigDefinition(NamedTuple):
    """Structure of a config option definition."""

    name: str
    default: Any
    type: type | Selector | vol.Coerce


class BasicConfig:
    """Basic configuration options."""

    MQTT_BROKER = ConfigDefinition("--mqtt-broker", None, str)
    MQTT_PORT = ConfigDefinition("--mqtt-port", 1883, int)
    MQTT_USER = ConfigDefinition("--mqtt-user", None, str)
    MQTT_PASSWORD = ConfigDefinition("--mqtt-password", None, str)
    MQTT_TLS = ConfigDefinition("--mqtt-tls", False, bool)  # noqa: FBT003
    MQTT_TLS_INSECURE = ConfigDefinition("--mqtt-tls-insecure", False, bool)  # noqa: FBT003
    DTU_HOST = ConfigDefinition("--dtu-host", None, str)
    DTU_PORT = ConfigDefinition("--dtu-port", 502, int)


LOG_LEVEL_OPTION = "--log-level"
LOG_TO_CONSOLE_OPTION = "--log-to-console"

ALL_MI_ENTITIES = [
    "grid_voltage",
    "grid_frequency",
    "temperature",
    "operating_status",
    "alarm_code",
    "alarm_count",
    "link_status",
]

MI_ENTITIES_SELECTOR = selector(
    {
        "select": {
            "options": ALL_MI_ENTITIES,
            "multiple": "true",
            "mode": "dropdown",
        },
    }
)

ALL_PORT_ENTITIES = [
    "pv_voltage",
    "pv_current",
    "pv_power",
    "today_production",
    "total_production",
]

PORT_ENTITIES_SELECTOR = selector(
    {
        "select": {
            "options": ALL_PORT_ENTITIES,
            "multiple": "true",
            "mode": "dropdown",
        },
    }
)


class ExtendedConfig:
    """Additional configuration options."""

    QUERY_PERIOD = ConfigDefinition("--query-period", 60, int)
    MI_ENTITIES = ConfigDefinition(
        "--mi-entities", ALL_MI_ENTITIES, MI_ENTITIES_SELECTOR
    )
    PORT_ENTITIES = ConfigDefinition(
        "--port-entities", ALL_PORT_ENTITIES, PORT_ENTITIES_SELECTOR
    )
    EXPIRE_AFTER = ConfigDefinition("--expire-after", 0, int)
    COMM_TIMEOUT = ConfigDefinition("--comm-timeout", 3, int)
    COMM_RETRIES = ConfigDefinition("--comm-retries", 0, int)
    COMM_RECONNECT_DELAY = ConfigDefinition(
        "--comm-reconnect-delay", 0.0, vol.Coerce(float)
    )
    COMM_RECONNECT_DELAY_MAX = ConfigDefinition(
        "--comm-reconnect-delay-max", 300.0, vol.Coerce(float)
    )


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
