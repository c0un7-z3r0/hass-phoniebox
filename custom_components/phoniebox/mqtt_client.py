# mypy: disable-error-code="attr-defined, unused-coroutine"
"""Creates the mqtt client."""

from collections.abc import Callable, Coroutine
from typing import Any

from homeassistant.components import mqtt
from homeassistant.components.mqtt.models import PublishPayloadType, ReceiveMessage
from homeassistant.core import HomeAssistant

from custom_components.phoniebox.const import LOGGER


class MqttClient:
    """MQTT Client to communicate with Phoniebox."""

    def __init__(self, hass: HomeAssistant, base_topic: str) -> None:
        """Init of the client."""
        self.base_topic = base_topic
        self.hass = hass

    async def async_subscribe(
        self,
        topic: str,
        msg_callback: Callable[[ReceiveMessage], Coroutine[Any, Any, None] | None],
    ) -> None:
        """
        Subscribe to the given topic.

        Adds the base_topic to the provided topic for convenience.
        """
        full_topic = f"{self.base_topic}/{topic}"
        await mqtt.async_subscribe(self.hass, full_topic, msg_callback)

    async def async_publish(self, topic: str, payload: PublishPayloadType) -> None:
        """Publish message to a MQTT topic for phoniebox."""
        full_topic = f"{self.base_topic}/{topic}"
        LOGGER.info("async_publish %(name)s", {"name": full_topic})
        await mqtt.async_publish(self.hass, full_topic, payload)

    async def async_publish_cmd(self, topic: str, payload: PublishPayloadType) -> None:
        """Send a command to phoniebox."""
        await self.async_publish(f"cmd/{topic}", payload)


__all__ = ["MqttClient"]
