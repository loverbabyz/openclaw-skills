---
description: Control native HomeKit IP devices directly via Bonjour/mDNS. Discover, pair, and control HomeKit accessories without Home Assistant.
---

# HomeKit Native Control

Use this skill when the user wants to control **native HomeKit devices** without Home Assistant or any bridge.

## Setup

**Requirements:**
- Python package `homekit` and `zeroconf` installed
- HomeKit devices on the same local network
- Devices must be in pairing mode (unpaired or reset)

**Installation:**
```bash
uv pip install homekit zeroconf
```

**Environment variables (optional):**
- `HOMEKIT_STORAGE` — path for pairing data (default: `~/.hermes/homekit_pairings.json`)

---

## Workflow

### Step 1: Discover Devices

```
homekit_discover(max_seconds=10)
```

Returns a list of discovered HomeKit devices with:
- `id` — device ID used for pairing
- `name` — Bonjour name
- `address` / `port` — IP connection info
- `model` — device model

**Example response:**
```json
{
  "result": [
    {
      "name": "My Light._hap._tcp.local.",
      "id": "AA:BB:CC:DD:EE:FF",
      "address": "192.168.1.100",
      "port": 5000,
      "model": "Light"
    }
  ]
}
```

### Step 2: Pair with a Device

The device must be in pairing mode (press and hold button on HomeKit device).

```
homekit_pair(alias="living_room_light", device_id="AA:BB:CC:DD:EE:FF", pin="123-45-678")
```

Use the PIN shown on the device (format: `XXX-YY-ZZZ`).

After pairing, the device is saved automatically.

### Step 3: List Accessories and Characteristics

```
homekit_list_accessories(alias="living_room_light")
```

Shows all accessories (aid), services, and characteristics (iid).

**Key characteristics by device type:**

| Device | Characteristic | Values |
|--------|---------------|--------|
| Light (on/off) | `1.8` (On) | `true` / `false` |
| Light (brightness) | `1.9` (Brightness) | `0-100` |
| Thermostat | `1.14` (Target Temperature) | number |
| Switch | `1.10` (On) | `true` / `false` |

> Use `homekit_get_characteristic` to find exact aid.iid values for your specific devices.

### Step 4: Read / Write Characteristics

**Read:**
```
homekit_get_characteristic(alias="living_room_light", characteristic="1.8")
```

**Write:**
```
homekit_put_characteristic(alias="living_room_light", characteristic="1.8", value=true)
```

---

## Helper Tools

- `homekit_list_pairings` — show all paired devices
- `homekit_unpair(alias="...")` — remove a pairing

---

## Notes

- HomeKit IP devices communicate via unicast HTTP on port 5000
- Discovery uses Bonjour/mDNS (`_hap._tcp.local.` service type)
- Pairing data persists in `HOMEKIT_STORAGE` file
- Some devices require the device to be in pairing mode within ~30 seconds of calling `homekit_pair`
- Cooldown between characteristic writes: ~100ms (built into HomeKit protocol)
