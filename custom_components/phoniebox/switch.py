"""Switch platform for phoniebox."""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory

from .const import (
    BINARY_SWITCHES,
    CONF_PHONIEBOX_NAME,
    DOMAIN,
    LOGGER,
    PHONIEBOX_ATTR_GPIO,
    PHONIEBOX_ATTR_RFID,
    PHONIEBOX_START,
    PHONIEBOX_STOP,
    TOPIC_DOMAIN_RANDOM,
    TOPIC_LENGTH_PLAYER_STATE,
)
from .entity import PhonieboxEntity
from .utils import (
    create_entity_slug,
    create_mqtt_context,
    handle_mqtt_entity_by_type,
)

if TYPE_CHECKING:
    from homeassistant.components.mqtt.models import ReceiveMessage
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data_coordinator import DataCoordinator


def discover_sensors(
    topic: str, entry: ConfigEntry, coordinator: DataCoordinator
) -> PhonieboxBinarySwitch | None:
    """Based on the topic and entry create the correct binary switch."""
    parts = topic.split("/")
    domain = parts[2] if len(parts) == TOPIC_LENGTH_PLAYER_STATE else parts[1]

    if domain not in BINARY_SWITCHES:
        return None

    if domain in [PHONIEBOX_ATTR_GPIO, PHONIEBOX_ATTR_RFID]:
        return PhonieboxBinarySwitch(
            config_entry=entry,
            coordinator=coordinator,
            data=SwitchData(
                name=domain,
                mqtt_topic=domain,
                mqtt_on_payload=PHONIEBOX_START,
                mqtt_off_payload=PHONIEBOX_STOP,
                entity_category=EntityCategory.CONFIG,
            ),
        )

    if domain == TOPIC_DOMAIN_RANDOM:
        return PhonieboxBinarySwitch(
            config_entry=entry,
            coordinator=coordinator,
            data=SwitchData(name=domain, mqtt_topic="playershuffle"),
        )

    return PhonieboxBinarySwitch(
        config_entry=entry,
        coordinator=coordinator,
        data=SwitchData(name=domain, mqtt_topic=domain),
    )


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
) -> None:
    """Set binary_sensor platform up."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    @callback
    def received_msg(msg: ReceiveMessage) -> None:
        sensors = discover_sensors(msg.topic, entry, coordinator)
        store = coordinator.switches

        if not sensors:
            return

        sensors_tuple = (
            (sensors,) if isinstance(sensors, PhonieboxBinarySwitch) else sensors
        )

        for sensor in sensors_tuple:
            context = create_mqtt_context(
                entity=sensor,
                store=store,
                hass=hass,
                msg_payload=msg.payload,
                async_add_entities_callback=async_add_devices,
            )
            handle_mqtt_entity_by_type(
                entity_type="switch",
                context=context,
            )

    await coordinator.mqtt_client.async_subscribe("#", received_msg)


def _slug(name: str, phoniebox_name: str) -> str:
    return create_entity_slug("switch", name, phoniebox_name)


@dataclass
class SwitchData:
    """Button Data."""

    name: str
    mqtt_topic: str | None = None
    mqtt_on_payload: str = ""
    mqtt_off_payload: str = ""
    entity_category: EntityCategory | None = None


class PhonieboxBinarySwitch(PhonieboxEntity, SwitchEntity, ABC):
    """phoniebox switch class."""

    # pylint: disable=too-many-instance-attributes

    _attr_should_poll = False

    def __init__(
        self, config_entry: ConfigEntry, coordinator: DataCoordinator, data: SwitchData
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, coordinator)
        self.entity_id = _slug(data.name, config_entry.data[CONF_PHONIEBOX_NAME])
        self._attr_name = data.name
        self._name = "switch_" + data.name
        self._mqtt_on_payload = data.mqtt_on_payload
        self._mqtt_off_payload = data.mqtt_off_payload
        self._mqtt_topic = data.mqtt_topic
        self._attr_entity_category = data.entity_category

    def set_state(self, *, value: bool) -> None:
        """Update the binary sensor with the most recent value."""
        if self._attr_is_on == value:
            return
        LOGGER.debug(
            "Updating switch %(name)s to -> %(value)s",
            {"name": self.name, "value": value},
        )
        self._attr_is_on = value

    async def async_turn_on(self, **kwargs: Any) -> None:  # noqa: ARG002
        """Turn the entity on."""
        await self.mqtt_client.async_publish(
            f"cmd/{self._mqtt_topic}", self._mqtt_on_payload
        )
        self.set_state(value=True)
        self.async_schedule_update_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:  # noqa: ARG002
        """Turn the entity on."""
        await self.mqtt_client.async_publish(
            f"cmd/{self._mqtt_topic}", self._mqtt_off_payload
        )
        self.set_state(value=False)
        self.async_schedule_update_ha_state()
