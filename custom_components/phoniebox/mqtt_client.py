import homeassistant.components.mqtt as mqtt


class MqttClient:
    """MQTT Client to communicate with Phoniebox-"""

    def __init__(self, hass, base_topic) -> None:
        self.base_topic = base_topic
        self.hass = hass

    async def async_subscribe(self, topic, msg_callback) -> None:
        full_topic = f"{self.base_topic}/{topic}"
        await mqtt.async_subscribe(self.hass, full_topic, msg_callback)

    async def async_publish(self, topic, payload) -> None:
        full_topic = f"{self.base_topic}/{topic}"
        await mqtt.async_publish(self.hass, full_topic, payload)

    async def async_publish_cmd(self, topic, payload) -> None:
        """ Send a command to phoniebox. """
        await self.async_publish(f"cmd/{topic}", payload)
