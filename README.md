# EmlaLock for Home Assistant

A custom Home Assistant integration for the [EmlaLock](https://emlalock.com) API.

## Features

- Easy setup through the Home Assistant UI.
- Supports multiple independent EmlaLock accounts/config entries.
- Supports wearer access and optional holder access.
- Session status and session information sensors.
- Live **Time remaining** and **Time passed** sensors.
- Minimum and maximum duration sensors.
- Requirement-link sensor.
- Add/remove time buttons for **1 hour** and **1 day**.
- Home Assistant services for changing time, minimum/maximum duration, and requirement links.
- Random-value services for minimum/maximum duration and requirement links.
- Uses the EmlaLock API as the source of truth for actions and permissions.

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
- **Holder API key** — optional. Add this when holder-authenticated actions are required.

The integration validates the credentials during setup. Each configured account has its own Home Assistant device and entities.

## Sensors

The integration provides sensors for:

- **Session** — whether a session is active.
- **Time remaining** — remaining session time, displayed as `DD HH MM SS`.
- **Time passed** — elapsed session time, displayed as `DD HH MM SS`.
- **Minimum duration** — configured minimum duration.
- **Maximum duration** — configured maximum duration.
- **Requirement links** — current requirement-link count.

Additional session information is available as attributes on the **Time remaining** sensor, including session ID, wearer, holder, status, start/end dates, duration, requirements, verification status, and cleaning status.

## Buttons

The integration provides four time-action buttons:

- **Add 1 hour**
- **Remove 1 hour**
- **Add 1 day**
- **Remove 1 day**

Remove buttons require holder access. The buttons send the current session start/end dates to the EmlaLock action API when available.

## Services

### Time

- `emlalock.add_time`
- `emlalock.subtract_time`

Single-value services use:

- `entry_id`
- `value`
- optional `text` for `add_time`

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

The EmlaLock server remains authoritative. If an action is not permitted, the API error is returned instead of the integration pretending the action succeeded.

## API

The integration communicates with the EmlaLock API at:

`https://api.emlalock.com`

It currently uses the EmlaLock information and action endpoints for session data, time, minimum/maximum duration, and requirement links.

## Requirements

- Home Assistant
- An EmlaLock account
- EmlaLock API credentials

## Support

For bugs, feature requests, or integration issues, open an issue in the repository:

https://github.com/walterz930/EmlaLock-hacs/issues

## License

See the repository for the current license and project information.
