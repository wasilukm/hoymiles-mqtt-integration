"""Constants for hoymiles-mqtt HA integration tests."""

from custom_components.mqtt_hoymiles.const import BasicConfig, ExtendedConfig

MOCK_CONFIG = {
    BasicConfig.DTU_HOST.name: "1.2.3.4",
    BasicConfig.DTU_PORT.name: 4321,
    BasicConfig.MQTT_BROKER.name: "3.4.5.6",
    BasicConfig.MQTT_PORT.name: 988,
    BasicConfig.MQTT_USER.name: "some_mqtt_user",
    BasicConfig.MQTT_PASSWORD.name: "some_password",
    BasicConfig.MQTT_TLS.name: False,
    BasicConfig.MQTT_TLS_INSECURE.name: False,
}

MOCK_OPTIONS = {
    ExtendedConfig.QUERY_PERIOD.name: 1,
    ExtendedConfig.MI_ENTITIES.name: ["grid_voltage"],
    ExtendedConfig.PORT_ENTITIES.name: ["pv_current"],
    ExtendedConfig.EXPIRE_AFTER.name: 2,
    ExtendedConfig.COMM_TIMEOUT.name: 3,
    ExtendedConfig.COMM_RETRIES.name: 4,
    ExtendedConfig.COMM_RECONNECT_DELAY.name: 5,
    ExtendedConfig.COMM_RECONNECT_DELAY_MAX.name: 6,
}
