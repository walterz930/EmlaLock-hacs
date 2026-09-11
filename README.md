# EmlaLock for Home Assistant

A custom Home Assistant integration for the [EmlaLock](https://emlalock.com) API.

## Features

- Easy setup through the Home Assistant UI.
- Supports multiple independent EmlaLock accounts/config entries.
- Supports wearer access and optional holder access.
- Binary **Session active** state plus session information sensors.
- Human-readable **Time remaining** and **Time passed** values using hours and lower units.
- Human-readable minimum and maximum duration values.
- Requirement-link sensor.
- Add/remove time buttons for **1 hour** and **1 day**.
- Home Assistant services for changing time, minimum/maximum duration, and requirement links.
- Random-value services for minimum/maximum duration and requirement links.
- Uses the documented EmlaLock API as the source of truth for actions, permissions, and errors.

## Sensors

Duration sensors are displayed in a compact human-readable format:

- `12h 30m 15s`
- `45m 20s`
- `12s`

The EmlaLock API itself continues to receive the values in its documented format; this change only affects how durations are displayed in Home Assistant.

## Buttons

The integration provides four time-action buttons:

- **Add 1 hour**
- **Remove 1 hour**
- **Add 1 day**
- **Remove 1 day**

Remove buttons are only enabled when holder access is configured. Buttons send only parameters documented by the corresponding EmlaLock endpoint.

## Services

### Time

- `emlalock.add_time`
- `emlalock.subtract_time`
- `emlalock.add_time_random`
- `emlalock.subtract_time_random`

Time values can be either seconds or EmlaLock short terms such as `W1D2H3M4S5`.

### Maximum duration

- `emlalock.add_maximum`
- `emlalock.subtract_maximum`
- `emlalock.add_maximum_random`
- `emlalock.subtract_maximum_random`

### Minimum duration

- `emlalock.add_minimum`
- `emlalock.subtract_minimum`
- `emlalock.add_minimum_random`
- `emlalock.subtract_minimum_random`

### Requirement links

- `emlalock.add_requirements`
- `emlalock.subtract_requirements`
- `emlalock.add_requirements_random`
- `emlalock.subtract_requirements_random`

The EmlaLock server remains authoritative for validation and permissions.

## Installation

### HACS

1. Open **HACS** in Home Assistant.
2. Open **Integrations**.
3. Search for **EmlaLock**.
4. Install the integration.
5. Restart Home Assistant.
6. Go to **Settings → Devices & services → Add integration** and search for **EmlaLock**.

If the repository is not yet available in the HACS default list, add this repository as a custom repository:

`https://github.com/walterz930/EmlaLock-hacs`

## API

The integration communicates with the EmlaLock API at:

`https://api.emlalock.com`

The API values remain compatible with the documented EmlaLock API. Only the Home Assistant presentation has been changed to show hours, minutes, and seconds instead of raw seconds.
