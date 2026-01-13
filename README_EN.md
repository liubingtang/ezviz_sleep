# EZVIZ Sleep Companion Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A custom Home Assistant integration for EZVIZ Sleep Companion devices.

## Features

- ✅ Real-time heart rate monitoring
- ✅ Real-time breathing rate monitoring
- ✅ Sleep status monitoring (Out of bed/Awake/Light sleep/Deep sleep/REM sleep)
- ✅ Body movement monitoring
- ✅ Sleep score
- ✅ Sleep duration statistics (Deep/Light/Awake)
- ✅ Multiple device support

## Installation

### Via HACS (Recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed
2. Click the three dots in the top right corner of HACS and select "Custom repositories"
3. Add this repository URL with category "Integration"
4. Search for "EZVIZ Sleep Companion" in HACS and install
5. Restart Home Assistant

### Manual Installation

1. Download this repository
2. Copy the `custom_components/ezviz_sleep` folder to your Home Assistant configuration directory's `custom_components` folder
3. Restart Home Assistant

## Configuration

1. In Home Assistant, go to "Configuration" -> "Integrations"
2. Click the "+ Add Integration" button in the bottom right
3. Search for "EZVIZ Sleep Companion"
4. Enter your EZVIZ Open Platform AppKey and AppSecret

### Getting AppKey and AppSecret

If you need to use the open platform API:

1. Visit [EZVIZ Open Platform](https://open.ys7.com/)
2. Register and login
3. Create an application to get AppKey and AppSecret

Note: This integration uses EZVIZ Open Platform API and requires AppKey and AppSecret.

## Sensors

The integration creates the following sensors for each sleep companion device:

| Sensor | Description | Unit |
|--------|-------------|------|
| Heart Rate | Real-time heart rate | bpm |
| Breath Rate | Real-time breathing rate | breaths/min |
| Sleep Status | Current sleep status | - |
| Body Movement | Body movement | - |
| Sleep Score | Sleep quality score | - |
| Deep Sleep | Deep sleep duration | minutes |
| Light Sleep | Light sleep duration | minutes |
| Awake Time | Awake duration | minutes |

## Usage Examples

### Display Sleep Data on Dashboard

```yaml
type: entities
title: Sleep Monitoring
entities:
  - entity: sensor.sleep_companion_heart_rate
  - entity: sensor.sleep_companion_breath_rate
  - entity: sensor.sleep_companion_sleep_status
  - entity: sensor.sleep_companion_sleep_score
```

### Create Automation

```yaml
automation:
  - alias: "Sleep Status Notification"
    trigger:
      - platform: state
        entity_id: sensor.sleep_companion_sleep_status
        to: "Deep Sleep"
    action:
      - service: notify.mobile_app
        data:
          message: "Entered deep sleep"
```

## Notes

1. This integration fetches data through EZVIZ Cloud API and requires internet connection
2. Data update interval is 5 minutes
3. Make sure your EZVIZ account has sleep companion devices bound
4. API endpoints may change; please submit an issue if you encounter problems

## FAQ

### Q: Cannot login to EZVIZ Cloud
A: Please check if your credentials are correct and ensure the account works normally in the EZVIZ app

### Q: Device not found
A: Make sure the device is properly added and working in the EZVIZ app

### Q: Data not updating
A: Check network connection and review Home Assistant logs for error messages

## Support

If you encounter issues or have suggestions, please submit them in [GitHub Issues](https://github.com/yourusername/ezviz_sleep/issues).

## License

MIT License

## Disclaimer

This is an unofficial integration and is not affiliated with EZVIZ. Users assume all responsibility for any issues arising from the use of this integration.
