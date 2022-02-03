"""BlueprintEntity class"""
from homeassistant.helpers.device_registry import CONNECTION_ZIGBEE
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION


class PhonieboxEntity(Entity):
    def __init__(self, config_entry, coordinator):
        self.config_entry = config_entry
        self.coordinator = coordinator
        self.mqtt_client = coordinator.mqtt_client

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + self.entity_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
            "sw_version": self.coordinator.version,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": self.config_entry.entry_id,
            "integration": DOMAIN,
        }
