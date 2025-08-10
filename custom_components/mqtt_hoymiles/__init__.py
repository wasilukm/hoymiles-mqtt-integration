"""
Custom integration to integrate hoymiles-mqtt with Home Assistant.

For more details about this integration, please refer to
https://github.com/wasilukm/hoymiles-mqtt-integration
"""

import logging
import traceback

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import (
    DOMAIN,
    LOG_LEVEL_OPTION,
    LOG_TO_CONSOLE_OPTION,
    NO_CONFIG_VALUE,
    STARTUP_MESSAGE,
)
from .manager import create_hoymiles_mqtt_process_manager

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    params = dict(entry.data)
    params[LOG_LEVEL_OPTION] = logging.getLevelName(_LOGGER.level)
    params[LOG_TO_CONSOLE_OPTION] = NO_CONFIG_VALUE
    params.update(dict(entry.options))

    monitor = await create_hoymiles_mqtt_process_manager(params=params)

    try:
        await monitor.start_process()
    except Exception as err:
        traceback.print_exception(err)
        raise ConfigEntryNotReady from err

    hass.data[DOMAIN][entry.entry_id] = monitor

    entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    monitor = hass.data[DOMAIN][entry.entry_id]
    del hass.data[DOMAIN][entry.entry_id]
    await monitor.terminate_process()
    return True


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle removal of an entry."""
    await async_unload_entry(hass, entry)


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
