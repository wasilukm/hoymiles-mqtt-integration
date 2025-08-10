"""Global fixtures for hoymiles-mqtt HA integration integration."""

from collections.abc import Generator
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:  # noqa: ARG001
    """Enable the custom integration fixture."""
    return


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss
# persistent notifications. These calls would fail without this fixture since
# the persistent_notification integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture() -> Generator:
    """Skip notification calls."""
    with (
        patch("homeassistant.components.persistent_notification.async_create"),
        patch("homeassistant.components.persistent_notification.async_dismiss"),
    ):
        yield


@pytest.fixture(name="proces_manager")
def reate_proces_manager_fixture() -> Generator:
    """Skip creating hoymiles_mqtt process."""
    with patch(
        "custom_components.mqtt_hoymiles.create_hoymiles_mqtt_process_manager"
    ) as mocked:
        yield mocked


# In this fixture, we are forcing calls to async_get_data to raise an Exception.
# This is useful for exception handling.
@pytest.fixture(name="error_on_get_data")
def error_get_data_fixture() -> Generator:
    """Simulate error when retrieving data from API."""
    with patch(
        "custom_components.mqtt_hoymiles.HoymilesMqttHaIntegrationApiClient.async_get_data",
        side_effect=Exception,
    ):
        yield
