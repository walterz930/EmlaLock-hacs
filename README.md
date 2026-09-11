# EmlaLock Home Assistant

Custom Home Assistant integration for the EmlaLock API.

## Features

- Multiple independent EmlaLock config entries.
- Wearer and key-holder access without a separate account-type selection.
- Session status, time remaining, minimum duration, maximum duration and requirement-link sensors.
- Add/subtract time buttons for 15 minutes, 1 hour and 1 day.
- Home Assistant services for all documented API mutation families: time, maximum duration, minimum duration and requirement links, including random variants.

## Installation

Copy `custom_components/emlalock` into the `custom_components` directory of your Home Assistant configuration, or install this repository as a custom HACS repository.

Restart Home Assistant and add EmlaLock from Settings > Devices & services.

## Configuration

Enter the EmlaLock User ID and API key. This creates a wearer instance.

If you also enter a Holder API key, the same User ID/API key are used as the target wearer credentials and the Holder API key is used for holder-authenticated actions. No account-type selection is required.

The config entries are independent and have their own devices/entities.

## Services

The integration registers:

- `emlalock.add_time`
- `emlalock.subtract_time`
- `emlalock.add_maximum`
- `emlalock.subtract_maximum`
- `emlalock.add_maximum_random`
- `emlalock.subtract_maximum_random`
- `emlalock.add_minimum`
- `emlalock.subtract_minimum`
- `emlalock.add_minimum_random`
- `emlalock.subtract_minimum_random`
- `emlalock.add_requirements`
- `emlalock.subtract_requirements`
- `emlalock.add_requirements_random`
- `emlalock.subtract_requirements_random`

Single-value services take `entry_id` and `value`; time services also accept an optional `text` field. Random services take `entry_id`, `from_value` and `to_value`.

The EmlaLock server remains authoritative: if an action is not permitted for the current account/session, its API error is surfaced rather than the integration pretending the action succeeded.

## API

The integration targets the documented EmlaLock API at `https://api.emlalock.com` and currently implements the documented `/info`, time, maximum-time, minimum-time and requirement-link endpoints.
