# Description

Home Assistant integration for Hoymiles Gateway DTU-Pro and DTU-Pro S devices. The integration is capable of gathering information from connected inverters, such as:
- Voltage
- Current
- Power
- Today's production
- Total production

and many more.

Connection to S-Miles Cloud is not required; the whole communication is local through ModbusTCP protocol.

This integration is a wrapper over https://github.com/wasilukm/hoymiles-mqtt tool for those who don't want or can't run the tool in isolation from Home Assistant. Therefore, the integration doesn't provide any entities or devices directly. Once the integration is properly configured, all devices (inverters and DTU) are visible under `MQTT` integration. They are named:
- `DTU_<serial_number>` - DTU device
- `inv_<serial_number>` - inverter instances

For more information, see https://github.com/wasilukm/hoymiles-mqtt project.

Migration between standalone `hoymiles-mqtt` and the integration is transparent. Although both solutions shall not be running at the same time.

`Disclaimer` This is an independent project, not affiliated with Hoymiles. Any trademarks or product names mentioned are the property of their respective owners.

# Prerequisities

- DTUs' Ethernet port connected to a network accesible by Home Assistant
- DTU has assigned IP address by DHCP server. IP address shall be reserved for the device
- Enabled MQTT integration and running MQTT broker, see https://www.home-assistant.io/integrations/mqtt/
