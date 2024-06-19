"""Tests for the Phoniebox Sensor."""

from typing import TYPE_CHECKING

from homeassistant.const import EntityCategory, UnitOfInformation, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_fire_mqtt_message,
)

if TYPE_CHECKING:
    from homeassistant.helpers.entity_registry import RegistryEntry

MOCK_VERSION = "2.2 - 305325d - master"


async def test_sensor_registry(
    hass: HomeAssistant,
    mock_phoniebox: MockConfigEntry,
    config: dict,
) -> None:
    """Test that a new sensor is created."""
    entity_registry = er.async_get(hass)
    er_items_before = er.async_entries_for_config_entry(
        entity_registry, mock_phoniebox.entry_id
    )

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/version", MOCK_VERSION)
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/last_card", "1234213")

    await hass.async_block_till_done()

    er_items_after = er.async_entries_for_config_entry(
        entity_registry, mock_phoniebox.entry_id
    )
    assert len(er_items_after) == len(er_items_before) + 2  # now added the sensor

    entry: RegistryEntry = entity_registry.async_get(
        "sensor.phoniebox_test_box_version"
    )
    assert entry
    assert entry.unique_id == "test_box-sensor.phoniebox_test_box_version"
    assert entry.entity_category == EntityCategory.DIAGNOSTIC

    version_sensor_state = hass.states.get("sensor.phoniebox_test_box_version")
    assert version_sensor_state is not None
    assert version_sensor_state.state == MOCK_VERSION

    last_card: RegistryEntry = entity_registry.async_get(
        "sensor.phoniebox_test_box_last_card"
    )
    assert last_card
    assert last_card.unique_id == "test_box-sensor.phoniebox_test_box_last_card"
    assert last_card.entity_category is None


async def test_sensor_registry_ignore_value(
    hass: HomeAssistant,
    mock_phoniebox: MockConfigEntry,
    config: dict,
) -> None:
    """Test that no new sensor is created for ignored values."""
    entity_registry = er.async_get(hass)
    er_items_before = er.async_entries_for_config_entry(
        entity_registry, mock_phoniebox.entry_id
    )

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", "0")
    await hass.async_block_till_done()

    er_items_after = er.async_entries_for_config_entry(
        entity_registry, mock_phoniebox.entry_id
    )
    assert len(er_items_after) == len(er_items_before)  # now added the sensor

    entry = entity_registry.async_get("sensor.phoniebox_test_box_volume")
    assert entry is None

    version_sensor_state = hass.states.get("sensor.phoniebox_test_box_volume")
    assert version_sensor_state is None


async def test_sensor_registry_update(
    hass: HomeAssistant, mock_phoniebox: MockConfigEntry, config: dict
) -> None:
    """Test that the sensor is updating properly on new value."""
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/version", MOCK_VERSION)
    await hass.async_block_till_done()
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/version", "2.3")
    await hass.async_block_till_done()

    version_sensor_state = hass.states.get("sensor.phoniebox_test_box_version")
    assert version_sensor_state is not None
    assert version_sensor_state.state != MOCK_VERSION
    assert version_sensor_state.state == "2.3"


async def test_temperature_sensor(
    hass: HomeAssistant, mock_phoniebox: MockConfigEntry, config: dict
) -> None:
    """Test that the sensor is updating properly on new value."""
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/temperature", "55.2'C")
    await hass.async_block_till_done()

    sensor_state = hass.states.get("sensor.phoniebox_test_box_temperature")
    assert sensor_state is not None
    assert sensor_state.state == "55.2"
    assert (
        sensor_state.attributes.get("unit_of_measurement") == UnitOfTemperature.CELSIUS
    )


async def test_gb_sensor(
    hass: HomeAssistant, mock_phoniebox: MockConfigEntry, config: dict
) -> None:
    """Test that the sensor is updating properly on new value."""
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/disk_avail", "5")
    await hass.async_block_till_done()

    sensor_state = hass.states.get("sensor.phoniebox_test_box_disk_avail")
    assert sensor_state is not None
    assert sensor_state.state == "5"
    assert (
        sensor_state.attributes.get("unit_of_measurement")
        == UnitOfInformation.GIGABYTES
    )


async def test_player_state_sensor(
    hass: HomeAssistant, mock_phoniebox: MockConfigEntry, config: dict
) -> None:
    """Test that the sensor is updating properly on new value."""
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/state", "play")
    await hass.async_block_till_done()

    sensor_state = hass.states.get("sensor.phoniebox_test_box_player_state")
    assert sensor_state is not None
    assert sensor_state.state == "play"


async def test_state_sensor(
    hass: HomeAssistant, mock_phoniebox: MockConfigEntry, config: dict
) -> None:
    """Test that the sensor is updating properly on new value."""
    async_fire_mqtt_message(hass, "test_phoniebox/state", "online")
    await hass.async_block_till_done()

    sensor_state = hass.states.get("sensor.phoniebox_test_box_state")
    assert sensor_state is not None
    assert sensor_state.state == "online"


async def test_spotify_source_sensor(
    hass: HomeAssistant, mock_phoniebox: MockConfigEntry, config: dict
) -> None:
    """Test that the sensor is updating properly on new value."""
    async_fire_mqtt_message(
        hass, "test_phoniebox/attribute/file", "spotify:playlist-id"
    )
    await hass.async_block_till_done()

    sensor_state = hass.states.get("sensor.phoniebox_test_box_source")
    assert sensor_state is not None
    assert sensor_state.state == "spotify"


async def test_file_source_sensor(
    hass: HomeAssistant, mock_phoniebox: MockConfigEntry, config: dict
) -> None:
    """Test that the sensor is updating properly on new value."""
    async_fire_mqtt_message(
        hass, "test_phoniebox/attribute/file", "file://path-to-file"
    )
    await hass.async_block_till_done()

    sensor_state = hass.states.get("sensor.phoniebox_test_box_source")
    assert sensor_state is not None
    assert sensor_state.state == "file"
