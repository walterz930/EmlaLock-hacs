# EmlaLock for Home Assistant

A custom Home Assistant integration for the [EmlaLock](https://emlalock.com) API, including a matching Lovelace dashboard card.

## Features

- Easy setup through the Home Assistant UI.
- Supports multiple independent EmlaLock accounts/config entries.
- Supports wearer access and optional holder access.
- Binary **Session active** state plus session information sensors.
- Human-readable **Time remaining** and **Time passed** values.
- Human-readable minimum and maximum duration values.
- Requirement-link sensor.
- Add/subtract time buttons for **1 hour** and **1 day**.
- Buttons become unavailable when `holder_api_key` is not configured.
- Optional EmlaLock Lovelace card styled like the mobile dashboard design.
- Home Assistant services for changing time, minimum/maximum duration, and requirement links.

## Lovelace card

The repository includes `www/emlalock-card.js`, a custom Lovelace card that automatically discovers the EmlaLock entities and buttons. It displays only the EmlaLock session information and the four duration controls.

The card automatically disables its duration buttons when the corresponding Home Assistant button entity is unavailable. The integration marks those entities unavailable when the holder API key is missing or there is no active session.

### Add the card resource once

Home Assistant requires custom frontend JavaScript to be registered as a Lovelace resource. Add this resource under **Settings → Dashboards → Resources**:

- URL: `/local/community/emlalock/www/emlalock-card.js`
- Resource type: `JavaScript module`

If HACS installs the repository under a different folder, use the matching `/local/community/<folder>/www/emlalock-card.js` path.

Then add a **Manual** card to the dashboard:

```yaml
type: custom:emlalock-card
```

No entity IDs or other card configuration are required. The card discovers the EmlaLock entities automatically.

## Sensors

The regular sensors are presented in this order:

1. Session
2. Start date
3. Time passed
4. End date
5. Time remaining
6. Maximum duration
7. Minimum duration
8. Requirement links

**Session active** is a binary sensor and is shown separately by Home Assistant.

## Buttons

The integration provides four time-action buttons:

- **Add 1 hour**
- **Subtract 1 hour**
- **Add 1 day**
- **Subtract 1 day**

They are unavailable unless holder access is configured and a session is active.

## Installation

### HACS

1. Open **HACS** in Home Assistant.
2. Open **Integrations**.
3. Search for **EmlaLock**.
4. Install or update the integration.
5. Restart Home Assistant.
6. Go to **Settings → Devices & services → Add integration** and search for **EmlaLock**.

If the repository is not yet available in the HACS default list, add this repository as a custom repository:

`https://github.com/walterz930/EmlaLock-hacs`

## API

The integration communicates with the EmlaLock API at:

`https://api.emlalock.com`

The API remains authoritative for validation, permissions, and errors.
