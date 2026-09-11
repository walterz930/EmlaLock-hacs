# EmlaLock for Home Assistant

A custom Home Assistant integration for the [EmlaLock](https://emlalock.com) API.

## Features

- Easy setup through the Home Assistant UI.
- Supports multiple independent EmlaLock accounts/config entries.
- Supports wearer access and optional holder access.
- Binary **Session active** state plus session information sensors.
- Native Home Assistant duration sensors for **Time remaining**, **Time passed**, **Minimum duration**, and **Maximum duration**.
- Requirement-link sensor.
- Add/remove time buttons for **1 hour** and **1 day**.
- Home Assistant services for changing time, minimum/maximum duration, and requirement links.
- Random-value services for minimum/maximum duration and requirement links.
- Uses the documented EmlaLock API as the source of truth for actions, permissions, and errors.

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

### Manual installation

Copy the `custom_components/emlalock` directory into your Home Assistant `custom_components` directory and restart Home Assistant.

## Configuration

Add EmlaLock from **Settings → Devices & services → Add integration**.

You will be asked for:

- **User ID** — your EmlaLock user ID.
- **API key** — your EmlaLock API key.
- **Holder API key** — optional. This is used for documented holder-authorized subtract operations.

The integration validates the wearer credentials against `/info` during setup. Each configured account has its own Home Assistant device and entities.

## Sensors

The integration provides:

- **Session** — `active` or `inactive`.
- **Session active** — Home Assistant binary state for whether the EmlaLock session is active.
- **Time remaining** — remaining session time as a native Home Assistant duration in seconds.
- **Time passed** — elapsed session time as a native Home Assistant duration in seconds.
- **Minimum duration** — configured minimum duration as a native duration.
- **Maximum duration** — configured maximum duration as a native duration.
- **Requirement links** — current requirement-link count.

The EmlaLock `/info` response remains available through entity state and attributes where useful, including session ID, wearer, holder, status, start/end dates, duration, requirements, verification, cleaning, and other session data.

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

Single-value time services use:

- `entry_id`
- `value`
- optional `text` for the time endpoints that support it

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

Random services use:

- `entry_id`
- `from_value`
- `to_value`

Requirement values are non-negative integers, matching the documented API.

The EmlaLock server remains authoritative. API errors such as `WrongAPIKey`, `NoActiveSession`, `SessionHasNoHolder`, `HolderNotFound`, and `InvalidTimeValue` are surfaced instead of being silently treated as successful actions.

## API

The integration communicates with the EmlaLock API at:

`https://api.emlalock.com`

The implementation follows the documented `/info`, time, maximum-duration, minimum-duration, and requirement-link endpoints. Holder API keys are only sent on documented holder-authorized subtract operations.

## Requirements

- Home Assistant
- An EmlaLock account
- EmlaLock API credentials

## Support

For bugs, feature requests, or integration issues, open an issue in the repository:

https://github.com/walterz930/EmlaLock-hacs/issues

## License

See the repository for the current license and project information.
