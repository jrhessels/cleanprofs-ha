# CleanProfs (Custom) – Home Assistant Integration

Custom Home Assistant integration to fetch CleanProfs planning data for a single address and expose it as entities.

## Features

- Fetches planning from the CleanProfs API (per address)
- Updates **once per day at 00:05** (Home Assistant local time)
- Creates fixed entities for:
  - `gft`
  - `rest`
  - `plastic`
- Case-insensitive matching against API product names (e.g. `GFT` matches `gft`)
- Single instance only (one address configuration)

## Entities

### Sensors (next pickup date)
- `sensor.cleanprofs_gft`
- `sensor.cleanprofs_rest`
- `sensor.cleanprofs_plastic`

State: `YYYY-MM-DD` (or `unknown` when not available)

### Binary sensor (any pickup today)
- `binary_sensor.cleanprofs_pickup_today`

State: `on` when any of the configured products has pickup **today**.  
Attributes include which products are due today (if implemented in your binary sensor).

### Calendar (optional)
If enabled/kept in code, a `calendar.*` entity can expose pickup dates as calendar events.  
(Some setups may choose not to link the calendar to the device page.)

## Installation (Manual)

1. Copy the integration folder to your Home Assistant config:
2. Restart Home Assistant.

3. Add the integration:
- Settings → Devices & services → Add integration → **CleanProfs**
- Enter `zipcode` and `house_number`

## Development / Testing (Windows + Docker)

Example test container:

```powershell
mkdir C:\ha-test\config -Force

docker run -d --name ha-test `
-p 8123:8123 `
-v C:\ha-test\config:/config `
--restart unless-stopped `
ghcr.io/home-assistant/home-assistant:stable

Restart Container:
docker restart ha-test

Logs: 
docker logs -f --since 0s ha-test | findstr /i cleanprofs