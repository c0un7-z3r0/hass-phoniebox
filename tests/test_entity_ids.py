"""Tests for valid entity IDs and stable unique IDs."""

import pytest
from homeassistant.core import HomeAssistant, valid_entity_id
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import frame
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_fire_mqtt_message,
)

from custom_components.phoniebox.const import (
    ALL_BUTTONS,
    CONF_MQTT_BASE_TOPIC,
    CONF_PHONIEBOX_NAME,
    DOMAIN,
)

ENTRY_ID = "entry_kinderzimmer"
MOCK_CONFIG_UPPERCASE = {
    CONF_PHONIEBOX_NAME: "Kinderzimmer",
    CONF_MQTT_BASE_TOPIC: "phoniebox1",
}


@pytest.fixture(autouse=True)
def reset_reported_usage() -> None:
    """Forget earlier reports, HA logs each deprecation only once per process."""
    frame._REPORTED_INTEGRATIONS.clear()  # noqa: SLF001


@pytest.fixture
def uppercase_config_entry() -> MockConfigEntry:
    """Return a config entry whose phoniebox name contains capitals."""
    return MockConfigEntry(
        title="Kinderzimmer",
        domain=DOMAIN,
        data=MOCK_CONFIG_UPPERCASE,
        entry_id=ENTRY_ID,
        unique_id="Phoniebox-Kinderzimmer",
    )


async def _setup_with_entities(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    async_fire_mqtt_message(hass, "phoniebox1/attribute/version", "2.9.0")
    async_fire_mqtt_message(hass, "phoniebox1/attribute/gpio", "true")
    await hass.async_block_till_done()


async def test_no_invalid_entity_id_warnings(
    hass: HomeAssistant,
    uppercase_config_entry: MockConfigEntry,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A name with capitals must not produce invalid or wrong-domain entity IDs."""
    await _setup_with_entities(hass, uppercase_config_entry)

    assert "sets an invalid entity ID" not in caplog.text
    assert "sets an entity ID with wrong domain" not in caplog.text

    entries = er.async_entries_for_config_entry(er.async_get(hass), ENTRY_ID)
    domains = {entry.domain for entry in entries}
    assert domains == {"media_player", "button", "sensor", "binary_sensor", "switch"}
    for entry in entries:
        assert valid_entity_id(entry.entity_id), entry.entity_id
        state = hass.states.get(entry.entity_id)
        assert state is not None, entry.entity_id
        assert state.entity_id == entry.entity_id


async def test_unique_ids_keep_previous_format(
    hass: HomeAssistant,
    uppercase_config_entry: MockConfigEntry,
) -> None:
    """Unique IDs must stay as before so existing registry entries are reused."""
    await _setup_with_entities(hass, uppercase_config_entry)
    registry = er.async_get(hass)

    expected = {
        "media_player.phoniebox_kinderzimmer": (
            f"{ENTRY_ID}-media_player.phoniebox_kinderzimmer"
        ),
        "button.phoniebox_kinderzimmer_shuffle": (
            f"{ENTRY_ID}-sensor.phoniebox_Kinderzimmer_shuffle"
        ),
        "sensor.phoniebox_kinderzimmer_version": (
            f"{ENTRY_ID}-sensor.phoniebox_Kinderzimmer_version"
        ),
        "binary_sensor.phoniebox_kinderzimmer_gpio": (
            f"{ENTRY_ID}-binary_sensor.phoniebox_Kinderzimmer_gpio"
        ),
        "switch.phoniebox_kinderzimmer_gpio": (
            f"{ENTRY_ID}-switch.phoniebox_Kinderzimmer_gpio"
        ),
    }
    for entity_id, unique_id in expected.items():
        entry = registry.async_get(entity_id)
        assert entry is not None, entity_id
        assert entry.unique_id == unique_id


async def test_existing_registry_entries_are_reused(
    hass: HomeAssistant,
    uppercase_config_entry: MockConfigEntry,
) -> None:
    """Entries registered by an earlier version keep their entity IDs."""
    uppercase_config_entry.add_to_hass(hass)
    registry = er.async_get(hass)
    old_button = registry.async_get_or_create(
        "button",
        DOMAIN,
        f"{ENTRY_ID}-sensor.phoniebox_Kinderzimmer_shuffle",
        suggested_object_id="phoniebox_kinderzimmer_shuffle",
        config_entry=uppercase_config_entry,
    )
    old_sensor = registry.async_get_or_create(
        "sensor",
        DOMAIN,
        f"{ENTRY_ID}-sensor.phoniebox_Kinderzimmer_version",
        suggested_object_id="phoniebox_kinderzimmer_version",
        config_entry=uppercase_config_entry,
    )
    count_before = len(er.async_entries_for_config_entry(registry, ENTRY_ID))

    assert await hass.config_entries.async_setup(ENTRY_ID)
    await hass.async_block_till_done()
    async_fire_mqtt_message(hass, "phoniebox1/attribute/version", "2.9.0")
    await hass.async_block_till_done()

    assert old_button.entity_id == "button.phoniebox_kinderzimmer_shuffle"
    assert old_sensor.entity_id == "sensor.phoniebox_kinderzimmer_version"
    assert hass.states.get("button.phoniebox_kinderzimmer_shuffle") is not None
    assert hass.states.get("sensor.phoniebox_kinderzimmer_version").state == "2.9.0"
    assert hass.states.get("button.phoniebox_kinderzimmer_shuffle_2") is None
    assert hass.states.get("sensor.phoniebox_kinderzimmer_version_2") is None
    # one media player, all buttons and the version sensor, without duplicates
    assert count_before == 2
    entries_after = er.async_entries_for_config_entry(registry, ENTRY_ID)
    assert len(entries_after) == 1 + len(ALL_BUTTONS) + 1
    assert not [e for e in entries_after if e.entity_id.endswith("_2")]
