"""BlueprintEntity class."""

from functools import cached_property
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION
from .data_coordinator import DataCoordinator


class PhonieboxEntity(Entity):
    """The phoniebox HA entity."""

    coordinator: DataCoordinator
    _unique_id_suffix: str | None = None

    def __init__(self, config_entry: ConfigEntry, coordinator: DataCoordinator) -> None:
        """Init the entity."""
        self.config_entry = config_entry
        self.coordinator = coordinator
        self.mqtt_client = coordinator.mqtt_client

    @cached_property
    def unique_id(self) -> str | None:
        """Return a unique ID to use for this entity."""
        suffix = self._unique_id_suffix or self.entity_id
        return f"{self.config_entry.entry_id}-{suffix}"

    @cached_property
    def device_info(self) -> DeviceInfo:
        """Returns the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_entry.entry_id)},
            name=NAME,
            model=VERSION,
            manufacturer=NAME,
            sw_version=self.coordinator.version,
        )

    @cached_property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": self.config_entry.entry_id,
            "integration": DOMAIN,
        }
