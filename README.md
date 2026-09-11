# EmlaLock Home Assistant

Custom Home Assistant integration for the EmlaLock API.

## Features

- Multiple independent EmlaLock config entries.
- Separate wearer and key-holder instances.
- Session status, time remaining, minimum duration, maximum duration and requirement-link sensors.
- Add/subtract time buttons for 15 minutes, 1 hour and 1 day.
- Home Assistant services for all documented API mutation families: time, maximum duration, minimum duration and requirement links, including random variants.
- Holder instances accept both the holder API key and wearer credentials so the documented holder-authenticated subtract endpoints can be used.

## Installation

Copy `custom_components/emlalock` into the `custom_components` directory of your Home Assistant configuration, or install this repository as a custom HACS repository.

Restart Home Assistant and add EmlaLock from Settings > Devices & services.

## Configuration

### Wearing instance

Enter the wearer's EmlaLock User ID and API key and choose `wearer`.

### Key-holder instance

Enter the holder's User ID and API key, choose `holder`, and also enter the wearer's User ID and API key. EmlaLock's holder-authenticated subtraction endpoints require the target wearer's credentials plus the holder API key.

The two config entries are independent and have their own devices/entities.

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
