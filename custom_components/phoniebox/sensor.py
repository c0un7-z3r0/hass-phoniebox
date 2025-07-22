"""Sensor platform for phoniebox."""

# pylint: disable=duplicate-code
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.mqtt.models import ReceiveMessage
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfInformation, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    BOOLEAN_SENSORS,
    CONF_PHONIEBOX_NAME,
    DIAGNOSTIC_SENSORS,
    DOMAIN,
    GIGABYTE_SENSORS,
    IGNORE_SENSORS,
    LOGGER,
    STRING_SENSORS,
    TOPIC_DOMAIN_FILE,
    TOPIC_DOMAIN_STATE,
    TOPIC_DOMAIN_TEMPERATUR,
    TOPIC_DOMAIN_VERSION,
    TOPIC_LENGTH_GENERIC_STATE,
    TOPIC_LENGTH_PLAYER_STATE,
)
from .data_coordinator import DataCoordinator
from .entity import PhonieboxEntity
from .utils import create_entity_slug, create_mqtt_context, handle_mqtt_entity_by_type


@dataclass
class SensorData:
    """Button Data."""

    name: str
    units: UnitOfInformation | UnitOfTemperature | None
    entity_category: EntityCategory | None = None
    icon: str | None = None
    device_class: SensorDeviceClass | None = None
    extract_value: Callable[[Any], float | str] | None = None


class GenericPhonieboxSensor(PhonieboxEntity, SensorEntity):  # pylint: disable=too-many-instance-attributes
    """Generic blueprint for a phoniebox sensor."""

    _attr_should_poll = False

    def __init__(
        self,
        config_entry: ConfigEntry,
        coordinator: DataCoordinator,
        data: SensorData,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, coordinator)
        self.entity_id = _slug(data.name, config_entry.data[CONF_PHONIEBOX_NAME])
        self._attr_name = data.name
        # This mqtt topic for the sensor which is its uid
        self._attr_native_unit_of_measurement = data.units
        self._attr_icon = data.icon
        self._attr_device_class = data.device_class
        self.extract_value = data.extract_value
        self._attr_entity_category = data.entity_category

    def set_state(self, *, value: bool) -> None:  # noqa: ARG002 # pylint: disable=unused-argument
        """Update the sensor with the most recent event."""
        return

    def set_event(self, event: Any) -> None:
        """Update the sensor with the most recent event."""
        value = event
        if self.extract_value is not None:
            value = self.extract_value(event)
        if self._attr_native_value == value:
            return

        LOGGER.debug(
            "Updating sensor %(name)s to -> %(value)s",
            {"name": self.name, "value": value},
        )
        self._attr_native_value = value


def is_player_state(domain: str, parts: list[str]) -> bool:
    """WIll check if received topic is player state update."""
    return domain == TOPIC_DOMAIN_STATE and len(parts) == TOPIC_LENGTH_PLAYER_STATE


def is_generic_state(domain: str, parts: list[str]) -> bool:
    """WIll check if received topic is a normal state update."""
    return domain == TOPIC_DOMAIN_STATE and len(parts) == TOPIC_LENGTH_GENERIC_STATE


def discover_sensors(  # noqa: PLR0911 # pylint: disable=too-many-return-statements
    topic: str,
    payload: Any,
    entry: Any,
    coordinator: Any,
) -> GenericPhonieboxSensor | None:
    """
    Given a topic, dynamically create the right sensor type.

    Async friendly.
    """
    parts = topic.split("/")
    domain = parts[2] if len(parts) == TOPIC_LENGTH_PLAYER_STATE else parts[1]

    if domain in IGNORE_SENSORS or domain in BOOLEAN_SENSORS:
        return None

    entity_category = (
        EntityCategory.DIAGNOSTIC if domain in DIAGNOSTIC_SENSORS else None
    )

    if domain == TOPIC_DOMAIN_TEMPERATUR:

        def temp_string_to_float(temp_str: str) -> float:
            return float(temp_str.split("'")[0])

        return GenericPhonieboxSensor(
            config_entry=entry,
            coordinator=coordinator,
            data=SensorData(
                name=domain,
                entity_category=entity_category,
                units=UnitOfTemperature.CELSIUS,
                device_class=SensorDeviceClass.TEMPERATURE,
                extract_value=temp_string_to_float,
            ),
        )

    if domain in GIGABYTE_SENSORS:
        return GenericPhonieboxSensor(
            config_entry=entry,
            coordinator=coordinator,
            data=SensorData(
                name=domain,
                units=UnitOfInformation.GIGABYTES,
                entity_category=entity_category,
            ),
        )

    if is_generic_state(domain, parts):
        return GenericPhonieboxSensor(
            config_entry=entry,
            coordinator=coordinator,
            data=SensorData(
                name="state",
                units=None,
                entity_category=entity_category,
            ),
        )
    if is_player_state(domain, parts):
        return GenericPhonieboxSensor(
            config_entry=entry,
            coordinator=coordinator,
            data=SensorData(
                name="player state",
                units=None,
                entity_category=entity_category,
            ),
        )

    if domain == TOPIC_DOMAIN_FILE:

        def find_source(file: str) -> str:
            return file.split(":")[0]

        return GenericPhonieboxSensor(
            config_entry=entry,
            coordinator=coordinator,
            data=SensorData(
                name="source",
                units=None,
                extract_value=find_source,
                entity_category=entity_category,
            ),
        )

    if domain == TOPIC_DOMAIN_VERSION:
        coordinator.version = payload

    if domain in STRING_SENSORS:
        return GenericPhonieboxSensor(
            config_entry=entry,
            coordinator=coordinator,
            data=SensorData(
                name=domain,
                units=None,
                entity_category=entity_category,
            ),
        )

    return None


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set the sensor platform up."""
    coordinator: DataCoordinator = hass.data[DOMAIN][entry.entry_id]

    @callback
    def received_msg(msg: ReceiveMessage) -> None:
        sensors = discover_sensors(msg.topic, msg.payload, entry, coordinator)
        store = coordinator.sensors

        if not sensors:
            return

        sensor_list = (
            (sensors,) if isinstance(sensors, GenericPhonieboxSensor) else sensors
        )

        for sensor in sensor_list:
            if not isinstance(sensor.name, str):
                continue

            context = create_mqtt_context(
                entity=sensor,
                store=store,
                hass=hass,
                msg_payload=msg.payload,
                async_add_entities_callback=async_add_entities,
            )
            handle_mqtt_entity_by_type(
                entity_type="sensor",
                context=context,
                debug_logger=LOGGER,
            )

    await coordinator.mqtt_client.async_subscribe("#", received_msg)


def _slug(name: str, phoniebox_name: str) -> str:
    return create_entity_slug("sensor", name, phoniebox_name)
