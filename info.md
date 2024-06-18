[![GitHub Release][releases-shield]][releases]
![GitHub commit activity][commits-shield]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

_Component to integrate your [phoniebox][phoniebox-repo] with [home-assistant][ha-website]._

![ha phoniebox mediaplayer](https://github.com/c0un7-z3r0/hass-phoniebox/blob/main/assets/media_player.png)

**Features**:

- add one or multiple phonieboxes as device to your home assistant
- media_player integration
- many sensors that are exposed via mqtt from phoniebox can be used
- enable / disable rfid or gpio from home assistant as configuration
- switch to toggle mute or random

## Requirements

- You will need to set up MQTT Broker in Home Assistant: [MQTT integration][ha_mqtt]
- You will need to set up MQTT on Phoniebox: [Phoniebox MQTT Installation][phoniebox_mqtt_setup]

## Installation

**Install via HACS**

1. Open _**HACS**_ and go to _**integrations**_
2. In the top right corner, click on the 3 dots and select Custom repositories
3. Add this repo URL https://github.com/c0un7-z3r0/hass-phoniebox and select **Integration** as category.
4. Back in **HACS**->**Integrations** click on Explore & Download Repositories in the bottom right corner
5. search for **phoniebox** and download the repository
6. Restart Home Assistant

**Manual Install**

If you want to install the custom component manually, add the folder `phoniebox/` to `YOUR_CONFIG_DIR/custom_components/`.

## Configuration is done in the UI

1. Once installed you can add your phoniebox as new device in Home Assistant
2. Go to **Configuration** -> **Devices & Service**
3. Add the phoniebox integration via the button in the bottom right

There are currently two settings that need configuration for the phoniebox. The name of the phoniebox
and the base MQTT Topic. This helps if you have multiple phonieboxes that you want to add to Home Assistant.

![ha phoniebox config](https://github.com/c0un7-z3r0/hass-phoniebox/blob/main/assets/configuration_options.png)

![ha phoniebox integration](https://github.com/c0un7-z3r0/hass-phoniebox/blob/main/assets/device.png)

- [Documentation on GitHub](https://github.com/c0un7-z3r0/hass-phoniebox/blob/main/README.md)
- [Report issues here](https://github.com/c0un7-z3r0/hass-phoniebox/issues)

<!---->

---

[hass-phoniebox]: https://github.com/c0un7-z3r0/hass-phoniebox
[commits-shield]: https://img.shields.io/github/commit-activity/w/c0un7-z3r0/hass-phoniebox?style=for-the-badge
[commits]: https://github.com/c0un7-z3r0/hass-phoniebox/commits/main
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[ha-forum]: https://community.home-assistant.io/
[ha-website]: https://www.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/c0un7-z3r0/hass-phoniebox?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40c0un7--z3r0-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/c0un7-z3r0/hass-phoniebox?style=for-the-badge
[releases]: https://github.com/c0un7-z3r0/hass-phoniebox/releases
[phoniebox-repo]: https://github.com/MiczFlor/RPi-Jukebox-RFID
[phoniebox_mqtt_setup]: https://github.com/MiczFlor/RPi-Jukebox-RFID/tree/develop/components/smart-home-automation/MQTT-protocol#installation
[ha_mqtt]: https://www.home-assistant.io/integrations/mqtt
