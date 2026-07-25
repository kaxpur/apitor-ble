# Apitor BLE Protocol

Reverse-engineered from the official **Apitor Kit** Android app
(`com.robot.apitor`). The relevant source is the decompiled class
`com.robot.apitor.robot.Robot` (plus `CommandBuilder` and `BluetoothActivity`).
This document describes the BLE profile, the connection/authorization sequence,
and the command frame formats.

> Scope: this covers the products that speak BLE. **Robot J** (product letter
> `j`, product index `6`) is the primary target and uses the standard
> motor/LED framing described below. "Wheels" (`w`) uses a slightly different
> framing that this library does not fully implement.

---

## 1. GATT profile

All Apitor products expose the same Nordic-UART-style service:

| Role                     | UUID                                   | 16-bit |
|--------------------------|----------------------------------------|--------|
| Service                  | `0000f0ff-0000-1000-8000-00805f9b34fb` | 0xF0FF |
| Write (phone → robot)    | `0000f001-0000-1000-8000-00805f9b34fb` | 0xF001 |
| Notify (robot → phone)   | `0000f002-0000-1000-8000-00805f9b34fb` | 0xF002 |

Link parameters used by the app (`BleManager` init):

- Writes are split into **≤20-byte chunks** (`setSplitWriteNum(20)`).
- Connect timeout **10 s**, per-operation timeout **5 s**, 1 reconnect attempt.
- Commands are throttled to roughly **one per 500 ms** (`CMD_INTERVAL_MS`).

---

## 2. Finding the robot

The scanner filters on the service UUID `0xF0FF` and then by **advertised
name**. A device belongs to a product if its name (case-insensitive, trimmed)
starts with:

```
"apitort" + <product letter>
```

For Robot J that prefix is **`apitortj`** (devices typically advertise as
`ApitorTJ-XXXX`).

Product-letter map (`ApitorPreference.getCurrentProdName`):

| Index | Letter | Product | Has BLE |
|------:|:------:|---------|:-------:|
| 0 | x | Robot X | yes |
| 1 | s | Robot S | yes |
| 2 | q | Robot Q | yes |
| 6 | **j** | **Robot J** | **yes** |
| 7 | r | Robot R | yes |
| 10 | w | Wheels | yes |

(Indexes 3,4,5,8,9,11,12 exist in the app but do not use BLE.)

---

## 3. Connection sequence

1. **Scan** with the service-UUID filter, match by name prefix.
2. **Connect** (GATT).
3. On connect success the app:
   a. **subscribes to notifications** on `0xF002`, and
   b. immediately writes the **authorization frame** (below) to `0xF001`.
4. Only after authorization does the robot act on motor/LED commands.

If the auth frame is not sent, the robot silently ignores all commands.

---

## 4. Authorization ("password") frame

A fixed 20-byte frame written once, right after connecting. Layout:

```
55 AA 11 20 43 6E 35 ... 7A   (Robot J)
│  │  │  │  └──────────────── 16 ASCII key bytes ("Cn5AtgZLJvqr8cDz")
│  │  │  └─────────────────── auth mode (20 = standard, 80 = Wheels)
│  │  └────────────────────── command (0x11 = authorize)
│  └───────────────────────── header byte 1
└──────────────────────────── header byte 0
```

(Wheels uses auth mode `80`, i.e. header `55 AA 11 80`, instead of `55 AA 11 20`.)

| Product | Full frame (hex)                                     | Key bytes (ASCII)  |
|---------|------------------------------------------------------|--------------------|
| **J**   | `55aa1120 436e354174675a4c4a7671723863447a`          | `Cn5AtgZLJvqr8cDz` |
| S       | `55aa1120 5572364f364d48524f6652416f4f5830`          | `Ur6O6MHROfRAoOX0` |
| Q       | `55aa1120 64796f7a574f50663035326757565034`          | `dyozWOPf052gWVP4` |
| R       | `55aa1120 633942527a6161317850307136696b62`          | `c9BRzaa1xP0q6ikb` |
| X       | `55aa1120 55494d384c5679526e75706973654276`          | `UIM8LVyRnupiseBv` |
| Wheels  | `55aa1180 686c354174675b7d4a7276723863447a`          | (non-printable)    |

Any product without its own key falls back to the **Robot X** key in the app.

---

## 5. Command frames

Commands are built by `CommandBuilder`: a type header followed by parameter
bytes. Robot J uses the plain motor/LED headers below. (Internally the app's
"Wheels" path uses a raw builder — `create(4)` — and manually prepends its own
`55AA..` headers; not needed for Robot J.)

### 5.1 Motor

```
55 AA 03 | <motor> <direction> <speed>
```

| Field     | Values |
|-----------|--------|
| motor     | `06`=M1, `07`=M2, `08`=M3, `09`=all, `10`(0x10)=stop-all |
| direction | `00`=stop, `01`=D1, `02`=D2 |
| speed     | `01`–`0C` (1–12, matches UI speeds S1–S12) |

Byte-by-byte (`55 AA 03 06 01 08` → motor M1, direction D1, speed 8):

```
55 AA 03 06 01 08
│  │  │  │  │  └─ speed      (0x08 = 8)
│  │  │  │  └──── direction  (0x01 = D1)
│  │  │  └─────── motor      (0x06 = M1)
│  │  └────────── command    (0x03 = motor)
│  └───────────── header byte 1
└──────────────── header byte 0
```

Examples:
- `55 AA 03 06 01 0A` → motor **M1**, direction **D1**, speed **10**
  (this is exactly what the app's built-in `Robot.test()` sends).
- **Stop all motors**: `55 AA 03 10 00 00`:

```
55 AA 03 10 00 00
│  │  │  │  │  └─ speed      (0 = off)
│  │  │  │  └──── direction  (0 = stop)
│  │  │  └─────── motor      (0x10 = stop-all)
│  │  └────────── command    (0x03 = motor)
│  └───────────── header byte 1
└──────────────── header byte 0
```

### 5.2 LED

```
55 AA 04 | <index> <color> 00 00
```

Two trailing zero bytes are always appended. Index selects the LED; the app
uses index `4` as an "all LEDs" shortcut.

Byte-by-byte (`55 AA 04 04 06 00 00` → all LEDs blue):

```
55 AA 04 04 06 00 00
│  │  │  │  │  │  └─ padding    (always 0)
│  │  │  │  │  └──── padding    (always 0)
│  │  │  │  └─────── color      (0x06 = blue)
│  │  │  └────────── index      (0x04 = all LEDs)
│  │  └───────────── command    (0x04 = LED)
│  └──────────────── header byte 1
└─────────────────── header byte 0
```

| Color  | Value | Color  | Value |
|--------|:-----:|--------|:-----:|
| Off    | 0     | Cyan   | 5     |
| Red    | 1     | Blue   | 6     |
| Orange | 2     | Purple | 7     |
| Yellow | 3     | White  | 10    |
| Green  | 4     |        |       |

### 5.3 Sensor / telemetry

- Sensor request/poll frames use the header `55 AA 05 80`.
- Incoming **notifications** (on `0xF002`) are parsed by `Robot.onMessage`:
  - Type 2 = sensor frame. Byte index `7` equal to `2` signals **low battery**.
  - The raw frame is otherwise forwarded to the app's Scratch/JS layer.

Byte-by-byte of a standard sensor notification (`55 AA 05 80 xx xx xx LL ...`):

```
55 AA 05 80 xx xx xx LL ...
│  │  │  │  └──┴──┴──┼── payload (relayed verbatim; meaning is per-attachment)
│  │  │  │           └── byte[7] = low-battery flag (LL: 2 = low)
│  │  │  └─────────────── sensor mode (0x80)
│  │  └────────────────── command (0x05 = sensor)
│  └───────────────────── header byte 1
└──────────────────────── header byte 0
```

This library decodes notifications via `apitor_ble.sensor.decode_notification`
into a `SensorFrame` (also delivered through `ApitorRobot.on_sensor(...)`):

| Field | Source | Notes |
|-------|--------|-------|
| `kind` | header match | `SENSOR` (`55AA0580`), `WHEELS`, or `UNKNOWN` |
| `low_power` | byte[7] == 2 (sensor) / byte[5] == 2 (wheels) | low-battery flag |
| `payload` | bytes after the 4-byte header | sensor frames only |
| `wheel_distance` / `order_buffer_size` / `order_action_end` | bytes 4/6/8 | **Wheels only** |

Only the low-battery flag has a firmware-confirmed meaning for Robot J; the
remaining sensor payload bytes are relayed verbatim by the app, so their
per-attachment meaning is left to the caller via `SensorFrame.payload` and the
raw bytes. Decoding never raises on short/unknown input — such frames come back
as `kind=UNKNOWN` with their raw bytes preserved.

---

## 6. Quick reference for Robot J

```
Service:  0000f0ff-0000-1000-8000-00805f9b34fb
Write:    0000f001-0000-1000-8000-00805f9b34fb   (split into 20-byte chunks)
Notify:   0000f002-0000-1000-8000-00805f9b34fb
Name:     starts with "ApitorTJ" (case-insensitive)

On connect:
  1. enable notify on f002
  2. write auth:  55AA1120 436E354174675A4C4A7671723863447A

Drive motor M1 forward at speed 8:   55AA03 06 01 08
Stop everything:                     55AA03 10 00 00
All LEDs blue:                       55AA04 04 06 00 00
```
