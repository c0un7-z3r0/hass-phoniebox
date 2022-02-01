"""Constants for phoniebox tests."""
from custom_components.phoniebox.const import CONF_PHONIEBOX_NAME, CONF_MQTT_BASE_TOPIC

# Mock config data to be used across multiple tests
MOCK_CONFIG = {CONF_PHONIEBOX_NAME: "test_box", CONF_MQTT_BASE_TOPIC: "test_phoniebox"}
