"""BlueprintEntity class"""
from typing import Any

from homeassistant.helpers.entity import Entity, DeviceInfo

from .data_coordinator import DataCoordinator
from .const import ATTRIBUTION, DOMAIN, NAME, VERSION


class PhonieboxEntity(Entity):
    coordinator: DataCoordinator

    def __init__(self, config_entry, coordinator: DataCoordinator):
        self.config_entry = config_entry
        self.coordinator = coordinator
        self.mqtt_client = coordinator.mqtt_client

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}-{self.entity_id}"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_entry.entry_id)},
            name=NAME,
            model=VERSION,
            manufacturer=NAME,
            sw_version=self.coordinator.version,
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": self.config_entry.entry_id,
            "integration": DOMAIN,
        }
