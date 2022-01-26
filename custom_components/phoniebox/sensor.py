"""Sensor platform for phoniebox."""
import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import DATA_GIGABYTES, TEMP_CELSIUS
from homeassistant.util import slugify

from .const import (
    BOOLEAN_SENSORS,
    CONF_PHONIEBOX_NAME,
    DOMAIN,
    GIGABYTE_SENSORS,
    IGNORE_SENSORS,
    NAME,
    STRING_SENSORS,
    VERSION,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)

DATA_PHONIEBOX = "data_phoniebox"


def discover_sensors(topic, payload, entry):
    """Given a topic, dynamically create the right sensor type.
    Async friendly.
    """
    parts = topic.split("/")
    domain = parts[2] if len(parts) == 3 else parts[1]
    if domain in IGNORE_SENSORS or domain in BOOLEAN_SENSORS:
        return

    if domain == "temperature":
        unit = TEMP_CELSIUS

        def temp_string_to_float(temp_str):
            return float(temp_str.split("'")[0])

        return GenericPhonieboxSensor(
            entry,
            topic,
            domain,
            unit,
            device_class=SensorDeviceClass.TEMPERATURE,
            extract_value=temp_string_to_float,
        )

    if domain in GIGABYTE_SENSORS:
        unit = DATA_GIGABYTES
        return GenericPhonieboxSensor(
            entry,
            topic,
            domain,
            unit,
        )

    if domain == "state" and len(parts) == 2:
        unit = None
        return GenericPhonieboxSensor(
            entry,
            topic,
            "state",
            unit,
        )
    if domain == "state" and len(parts) == 3:
        unit = None
        return GenericPhonieboxSensor(
            entry,
            topic,
            "player state",
            unit,
        )

    if domain == "file":
        unit = None

        def find_source(file):
            return file.split(":")[0]

        return GenericPhonieboxSensor(
            entry, topic, "source", unit, extract_value=find_source
        )

    if domain in STRING_SENSORS:
        unit = None
        return GenericPhonieboxSensor(entry, topic, domain, unit)
    _LOGGER.info(
        "-> Potential new sensor %(domain)s => %(payload)s",
        {"domain": domain, "payload": payload},
    )


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    def received_msg(msg):
        sensors = discover_sensors(msg.topic, msg.payload, entry)
        store = coordinator.sensors

        if not sensors:
            return

        if isinstance(sensors, GenericPhonieboxSensor):
            sensors = (sensors,)

        for sensor in sensors:
            if sensor.name not in store:
                sensor.hass = hass
                sensor.set_event(msg.payload)
                store[sensor.name] = sensor
                _LOGGER.debug("Registering sensor %(name)s", {"name": sensor.name})
                async_add_devices((sensor,), True)
            else:
                store[sensor.name].set_event(msg.payload)

    await coordinator.mqtt_client.async_subscribe("#", received_msg)


def string_to_bool(value):
    """
    boolean string to boolean converter
    """
    if value == "true":
        return True
    else:
        return False


def _slug(name, poniebox_name):
    return f"sensor.phoniebox_{poniebox_name}_{slugify(name)}"


class GenericPhonieboxSensor(SensorEntity):
    """Generic blueprint for a phoniebox sensor"""

    _attr_should_poll = False

    def __init__(
        self,
        config_entry,
        topic,
        name,
        units,
        icon=None,
        device_class=None,
        extract_value=None,
    ):
        """Initialize the sensor."""
        self.config_entry = config_entry
        self.entity_id = _slug(name, config_entry.data[CONF_PHONIEBOX_NAME])
        self._attr_name = name
        # This mqtt topic for the sensor which is its uid
        self._attr_unique_id = config_entry.entry_id + self.entity_id
        self._attr_native_unit_of_measurement = units
        self._attr_icon = icon
        self._attr_device_class = device_class
        self.extract_value = extract_value

    def set_event(self, event):
        """Update the sensor with the most recent event."""
        value = event
        if self.extract_value is not None:
            value = self.extract_value(event)
        self._attr_native_value = value
        self.async_write_ha_state()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
        }
