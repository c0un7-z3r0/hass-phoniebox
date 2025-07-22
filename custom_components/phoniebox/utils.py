"""Utility functions."""

from dataclasses import dataclass
from typing import Any

from homeassistant.util import slugify


@dataclass
class MqttEntityConfig:  # pylint: disable=too-many-instance-attributes
    """Configuration for MQTT entity discovery and management."""

    entity: Any
    store: dict[str, Any]
    hass: Any
    payload: Any
    async_add_entities_callback: Any
    is_event_based: bool = False
    debug_logger: Any = None
    entity_type_name: str = "entity"


@dataclass
class MqttContext:
    """Common MQTT context parameters for entity discovery."""

    entity: Any
    store: dict[str, Any]
    hass: Any
    payload: Any
    async_add_entities_callback: Any


def string_to_bool(value: str) -> bool:
    """Boolean string to boolean converter."""
    return value == "true"


def bool_to_string(value: bool) -> str:  # noqa: FBT001
    """Boolean string to boolean converter."""
    if value:
        return "true"
    return "false"


def parse_float_save(val: Any, fallback: float = 0.0) -> float:
    """Try to parse value to float or return fallback."""
    try:
        return float(val)
    except ValueError:
        return fallback


def parse_int_save(val: Any, fallback: int = 0) -> int:
    """Try to parse value to int or return fallback."""
    try:
        return int(val)
    except ValueError:
        return fallback


def ensure_entity_hass_and_update_state(
    entity: Any, hass: Any, payload: Any, *, is_event_based: bool = False
) -> None:
    """
    Ensure entity has hass attribute set and update its state.

    This utility function prevents the 'Attribute hass is None' runtime error
    by ensuring the hass attribute is properly set before scheduling state updates.

    Args:
    ----
        entity: The entity to update
        hass: Home Assistant instance
        payload: MQTT payload
        is_event_based: Whether to use set_event (True) or set_state (False)

    """
    # Ensure hass attribute is set before scheduling state update
    if entity.hass is None:
        entity.hass = hass

    if is_event_based:
        entity.set_event(payload)
    else:
        entity.set_state(value=string_to_bool(str(payload)))

    entity.async_schedule_update_ha_state()


def create_entity_slug(entity_type: str, name: str, phoniebox_name: str) -> str:
    """Create a standardized entity slug for phoniebox entities."""
    return f"{entity_type}.phoniebox_{phoniebox_name}_{slugify(name)}"


def create_mqtt_context(
    entity: Any,
    store: dict[str, Any],
    hass: Any,
    msg_payload: Any,
    async_add_entities_callback: Any,
) -> MqttContext:
    """Create a standard MqttContext object."""
    return MqttContext(
        entity=entity,
        store=store,
        hass=hass,
        payload=msg_payload,
        async_add_entities_callback=async_add_entities_callback,
    )


def handle_mqtt_entity_by_type(
    entity_type: str,
    context: MqttContext,
    debug_logger: Any = None,
) -> None:
    """
    Handle MQTT entity discovery with type-specific configuration.

    This function reduces code duplication by automatically configuring
    entities based on their type.
    """
    # Configure based on entity type
    if entity_type == "switch":
        config = MqttEntityConfig(
            entity=context.entity,
            store=context.store,
            hass=context.hass,
            payload=context.payload,
            async_add_entities_callback=context.async_add_entities_callback,
            is_event_based=False,
        )
    elif entity_type == "binary_sensor":
        config = MqttEntityConfig(
            entity=context.entity,
            store=context.store,
            hass=context.hass,
            payload=context.payload,
            async_add_entities_callback=context.async_add_entities_callback,
            is_event_based=False,
            debug_logger=debug_logger,
            entity_type_name="binary sensor",
        )
    elif entity_type == "sensor":
        config = MqttEntityConfig(
            entity=context.entity,
            store=context.store,
            hass=context.hass,
            payload=context.payload,
            async_add_entities_callback=context.async_add_entities_callback,
            is_event_based=True,
            debug_logger=debug_logger,
            entity_type_name="sensor",
        )
    else:
        msg = f"Unknown entity type: {entity_type}"
        raise ValueError(msg)

    handle_mqtt_entity_discovery(config)


def handle_mqtt_entity_discovery(config: MqttEntityConfig) -> None:
    """
    Handle MQTT entity discovery and state updates.

    This function encapsulates the complete MQTT entity management pattern:
    1. Check if entity exists in store
    2. Add new entity or update existing one
    3. Ensure hass attribute is properly set
    4. Schedule state updates

    Args:
    ----
        config: Configuration object containing all required parameters

    """
    if config.entity.name not in config.store:
        config.entity.hass = config.hass
        if config.is_event_based:
            config.entity.set_event(config.payload)
        else:
            config.entity.set_state(value=string_to_bool(str(config.payload)))
        config.store[config.entity.name] = config.entity
        if config.debug_logger:
            config.debug_logger.debug(
                "Registering %(entity_type)s %(name)s",
                {"entity_type": config.entity_type_name, "name": config.entity.name},
            )
        config.async_add_entities_callback(
            new_entities=(config.entity,), update_before_add=True
        )
    else:
        ensure_entity_hass_and_update_state(
            config.store[config.entity.name],
            config.hass,
            config.payload,
            is_event_based=config.is_event_based,
        )
