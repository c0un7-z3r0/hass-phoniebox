"""Tests for the Phoniebox Sensor."""
from homeassistant.const import DATA_GIGABYTES, TEMP_CELSIUS
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_registry import RegistryEntry
from pytest_homeassistant_custom_component.common import async_fire_mqtt_message

MOCK_VERSION = "2.2 - 305325d - master"


async def test_sensor_registry(
    hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config
):
    """Test that a new sensor is created"""
    entity_registry = er.async_get(hass)
    er_items_before = er.async_entries_for_config_entry(
        entity_registry, mock_phoniebox.entry_id
    )

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/version", MOCK_VERSION)
    await hass.async_block_till_done()

    er_items_after = er.async_entries_for_config_entry(
        entity_registry, mock_phoniebox.entry_id
    )
    assert len(er_items_after) == len(er_items_before) + 1  # now added the sensor

    entry: RegistryEntry = entity_registry.async_get(
        "sensor.phoniebox_test_box_version"
    )
    assert entry
    assert entry.unique_id == "test_box-sensor.phoniebox_test_box_version"

    version_sensor_state = hass.states.get("sensor.phoniebox_test_box_version")
    assert version_sensor_state is not None
    assert version_sensor_state.state == MOCK_VERSION


async def test_sensor_registry_ignore_value(
    hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config
):
    """Test that no new sensor is created for ignored values"""
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

    entry: RegistryEntry = entity_registry.async_get(
        "sensor.phoniebox_test_box_volume"
    )
    assert entry is None

    version_sensor_state = hass.states.get("sensor.phoniebox_test_box_volume")
    assert version_sensor_state is None


async def test_sensor_registry_update(
    hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config
):
    """Test that the sensor is updating properly on new value"""
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/version", MOCK_VERSION)
    await hass.async_block_till_done()
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/version", "2.3")
    await hass.async_block_till_done()

    version_sensor_state = hass.states.get("sensor.phoniebox_test_box_version")
    assert version_sensor_state is not None
    assert version_sensor_state.state != MOCK_VERSION
    assert version_sensor_state.state == "2.3"


async def test_temperature_sensor(
    hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config
):
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/temperature", "55.2'C")
    await hass.async_block_till_done()

    sensor_state = hass.states.get("sensor.phoniebox_test_box_temperature")
    assert sensor_state is not None
    assert sensor_state.state == "55.2"
    assert sensor_state.attributes.get("unit_of_measurement") == TEMP_CELSIUS


async def test_gb_sensor(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/disk_avail", "5")
    await hass.async_block_till_done()

    sensor_state = hass.states.get("sensor.phoniebox_test_box_disk_avail")
    assert sensor_state is not None
    assert sensor_state.state == "5"
    assert sensor_state.attributes.get("unit_of_measurement") == DATA_GIGABYTES


async def test_player_state_sensor(
    hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config
):
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/state", "play")
    await hass.async_block_till_done()

    sensor_state = hass.states.get("sensor.phoniebox_test_box_player_state")
    assert sensor_state is not None
    assert sensor_state.state == "play"


async def test_state_sensor(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    async_fire_mqtt_message(hass, "test_phoniebox/state", "online")
    await hass.async_block_till_done()

    sensor_state = hass.states.get("sensor.phoniebox_test_box_state")
    assert sensor_state is not None
    assert sensor_state.state == "online"


async def test_spotify_source_sensor(
    hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config
):
    async_fire_mqtt_message(
        hass, "test_phoniebox/attribute/file", "spotify:playlist-id"
    )
    await hass.async_block_till_done()

    sensor_state = hass.states.get("sensor.phoniebox_test_box_source")
    assert sensor_state is not None
    assert sensor_state.state == "spotify"


async def test_file_source_sensor(
    hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config
):
    async_fire_mqtt_message(
        hass, "test_phoniebox/attribute/file", "file://path-to-file"
    )
    await hass.async_block_till_done()

    sensor_state = hass.states.get("sensor.phoniebox_test_box_source")
    assert sensor_state is not None
    assert sensor_state.state == "file"
