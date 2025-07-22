# HA Phoniebox

[![GitHub Release][releases-shield]][releases]
![GitHub commit activity][commits-shield]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
![Project Maintenance](https://img.shields.io/maintenance/yes/2025.svg?style=for-the-badge)
[![Validate](https://github.com/c0un7-z3r0/hass-phoniebox/actions/workflows/validate-changes.yml/badge.svg)](https://github.com/c0un7-z3r0/hass-phoniebox/actions/workflows/validate-changes.yml)

_Component to integrate your [phoniebox][phoniebox-repo] with [Home Assistant][ha-website]._

## Table of Contents

- [Features](#features)
- [How does it work](#how-does-it-work)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration-is-done-in-the-ui)
- [Compatibility](#compatibility)
- [Troubleshooting](#troubleshooting)
- [Issues](#issues)
- [Contributing](#contributing)

![ha phoniebox mediaplayer](https://github.com/c0un7-z3r0/hass-phoniebox/blob/main/assets/media_player.png)

**Features**:

- **Multi-device Support**: Add one or multiple Phonieboxes as devices to your Home Assistant
- **Media Player Integration**: Full media player entity with play/pause/stop/volume controls
- **Rich Sensor Data**: Many sensors exposed via MQTT from Phoniebox including:
  - Current playing track information
  - Volume levels
  - Player state (playing, paused, stopped)
  - RFID card detection
  - GPIO button states
- **Remote Configuration**: Enable/disable RFID or GPIO directly from Home Assistant
- **Audio Control**: Switch entities to toggle mute or random playback modes
- **Real-time Updates**: All state changes are pushed via MQTT for instant updates

Overview of what Features of Phoniebox have been implemented can be found in
the [issues](https://github.com/c0un7-z3r0/hass-phoniebox/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement).

## How does it work

Once the custom component is installed you can add your phoniebox as device in home assistant.
You can name your phoniebox and configure the MQTT base topic in case you have multiple phonieboxes.

All communication with Phoniebox is running over MQTT.

## Requirements

> **⚠️ Important**: Both MQTT integrations must be properly configured before installing this integration.

- **Home Assistant MQTT Integration**: [MQTT integration][ha_mqtt] must be installed and configured
- **Phoniebox MQTT Support**: [Phoniebox MQTT Installation][phoniebox_mqtt_setup] must be completed on your Phoniebox
- A working MQTT broker (like Mosquitto) accessible by both Home Assistant and your Phoniebox

## Installation

**Install via HACS**

1. Open **HACS** in your Home Assistant instance
2. Go to **Integrations**
3. Click **Explore & Download Repositories** in the bottom right corner
4. Search for **Phoniebox**
5. Click on the **Phoniebox** integration
6. Click **Download** and then **Download** again to confirm
7. Restart Home Assistant

**Manual Install**

If you want to install the custom component manually, add the folder `phoniebox/` to `YOUR_CONFIG_DIR/custom_components/`.

## Configuration is done in the UI

1. Once installed, you can add your Phoniebox as a new device in Home Assistant
2. Go to **Settings** → **Devices & Services**
3. Click **Add Integration** in the bottom right corner
4. Search for **Phoniebox** and select it

There are currently two settings that need configuration for the phoniebox. The name of the phoniebox
and the base MQTT Topic. This helps if you have multiple phonieboxes that you want to add to Home Assistant.

![ha phoniebox config](https://github.com/c0un7-z3r0/hass-phoniebox/blob/main/assets/configuration_options.png)

![ha phoniebox integration](https://github.com/c0un7-z3r0/hass-phoniebox/blob/main/assets/device.png)

## Compatibility

This integration is compatible with:
- Home Assistant 2023.1 and later
- Phoniebox 2.0 and later
- Python 3.11+

## Troubleshooting

### Common Issues

**MQTT Connection Issues**
- Ensure your MQTT broker is properly configured in Home Assistant
- Verify that Phoniebox is publishing to the correct MQTT topics
- Check that the base MQTT topic matches between Phoniebox and the integration

**Device Not Appearing**
- Restart Home Assistant after installation
- Check that MQTT discovery is enabled in your Home Assistant configuration
- Verify Phoniebox MQTT configuration is working correctly

**Media Player Not Responding**
- Ensure Phoniebox web interface is accessible
- Check MQTT message logs in Home Assistant
- Verify that all required MQTT topics are being published by Phoniebox

For more troubleshooting help, check the [issues](https://github.com/c0un7-z3r0/hass-phoniebox/issues) page.

## Issues

When you experience issues/bugs with this, the best way to report them is to open an issue in this repo.

[Report issues here](https://github.com/c0un7-z3r0/hass-phoniebox/issues)

<!---->

## Contributing

Contributions are welcome! Here's how you can help:

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/c0un7-z3r0/hass-phoniebox.git
   cd hass-phoniebox
   ```

2. **Install development dependencies**
   ```bash
   ./scripts/setup_tests
   ```

3. **Run tests**
   ```bash
   pytest
   ```

4. **Run linting**
   ```bash
   pre-commit run --all-files
   ```

### How to Contribute

- **Bug Reports**: Use the [issue tracker](https://github.com/c0un7-z3r0/hass-phoniebox/issues) to report bugs
- **Feature Requests**: Submit enhancement requests via GitHub issues
- **Pull Requests**: Fork the repo and submit PRs for bug fixes or new features
- **Documentation**: Help improve documentation and examples

### Code Style

This project follows:
- [PEP 8](https://pep8.org/) for Python code style
- [Conventional Commits](https://conventionalcommits.org/) for commit messages
- Type hints are required for all public functions
- Tests are required for new features

## Contributions are welcome!

---

[commits-shield]: https://img.shields.io/github/commit-activity/w/c0un7-z3r0/hass-phoniebox?style=for-the-badge
[ha_mqtt]: https://www.home-assistant.io/integrations/mqtt
[ha-website]: https://www.home-assistant.io/
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/c0un7-z3r0/hass-phoniebox?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40c0un7--z3r0-blue.svg?style=for-the-badge
[phoniebox_mqtt_setup]: https://github.com/MiczFlor/RPi-Jukebox-RFID/tree/develop/components/smart-home-automation/MQTT-protocol#installation
[phoniebox-repo]: https://github.com/MiczFlor/RPi-Jukebox-RFID
[releases]: https://github.com/c0un7-z3r0/hass-phoniebox/releases
[releases-shield]: https://img.shields.io/github/release/c0un7-z3r0/hass-phoniebox?style=for-the-badge
