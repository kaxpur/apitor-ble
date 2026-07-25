# Using `apitor_ble`

## Install

From the project root:

```bash
pip install -e .          # installs the package + bleak
# or just the runtime dep:
pip install -r requirements.txt
```

Requires Python 3.10+ and a working Bluetooth LE adapter. `bleak` supports
Windows, macOS, and Linux (BlueZ).

## Quick start

```python
import asyncio
from apitor_ble import ApitorRobot, Motor, Direction, Color

async def main():
    # Scan for and connect to the first Robot J in range.
    robot = await ApitorRobot.discover(product="j")
    async with robot:                      # connects + authorizes; disconnects on exit
        await robot.run_motor(Motor.M1, Direction.D1, speed=8)
        await asyncio.sleep(2)
        await robot.stop_all_motors()
        await robot.all_leds(Color.BLUE)

asyncio.run(main())
```

## API overview

### Discovery

```python
devices = await ApitorRobot.scan(product="j", timeout=10.0)   # list[BLEDevice]
robot   = await ApitorRobot.discover(product="j")             # first match, ready to connect
robot   = ApitorRobot(address="AA:BB:CC:DD:EE:FF", product="j")  # skip scanning
```

### Connection

```python
await robot.connect()        # connect, subscribe to notifications, send auth
robot.is_connected           # bool
await robot.disconnect()

async with robot:            # preferred: auto connect/disconnect
    ...
```

### Movement

```python
await robot.run_motor(Motor.M1, Direction.D1, speed=8)   # speed 0-12
await robot.stop_motor(Motor.M1)
await robot.stop_all_motors()
```

`Motor` = `M1, M2, M3, ALL`. `Direction` = `D1, D2, STOP`.

### LEDs

```python
await robot.set_led(index=1, color=Color.RED)
await robot.all_leds(Color.GREEN)        # index 4 = all
await robot.all_leds(Color.OFF)
```

Available colors (`Color` enum):

| Name | Value |
|--------|-------|
| `OFF` | 0 |
| `RED` | 1 |
| `ORANGE` | 2 |
| `YELLOW` | 3 |
| `GREEN` | 4 |
| `CYAN` | 5 |
| `BLUE` | 6 |
| `PURPLE` | 7 |
| `WHITE` | 10 |

Values 8 and 9 are unused; the numbering jumps from `PURPLE` (7) to `WHITE` (10).

### Notifications (sensor / status frames)

Decoded frames (recommended):

```python
from apitor_ble import SensorFrame

def on_sensor(frame: SensorFrame):
    print(frame)                      # SensorFrame(kind=SENSOR, hex=..., LOW_POWER)
    if frame.low_power:
        print("battery low!")

robot.on_sensor(on_sensor)
await robot.connect()
# robot.low_power  -> last known low-battery state (or None)
```

Raw bytes, if you prefer to decode yourself:

```python
robot.on_notify(lambda raw: print("robot sent:", raw.hex()))
```

You can also decode standalone frames without a connection:

```python
from apitor_ble import decode_notification
frame = decode_notification(bytes.fromhex("55aa0580000002000000"))
```

### Raw access

If you need a frame this library doesn't wrap:

```python
await robot.send_raw(bytes.fromhex("55AA0306010A"))   # auto-chunked to 20 bytes
```

The `apitor_ble.protocol` module also exposes pure frame-builders with no I/O:
`auth_frame`, `motor_command`, `stop_all_command`, `led_command`,
`device_name_matches`, `chunk_write`.

## Test harness (`main.py`)

```bash
python main.py scan                  # list nearby Robot J devices
python main.py demo                  # motors + LED sequence
python main.py listen                # print incoming notification frames
python main.py drive                 # keyboard control (type key + Enter)

python main.py demo --address AA:BB:CC:DD:EE:FF   # skip scanning
python main.py scan --product s      # a different Apitor product
python main.py demo --verbose        # log raw TX/RX frames
```

## Troubleshooting

- **No devices found** — make sure the robot is on, the battery is charged, and
  Bluetooth is enabled. On Linux, BlueZ scanning may need appropriate
  permissions. On Windows, ensure the app has Bluetooth access.
- **Connects but doesn't move** — the auth frame must be sent first. Using
  `connect()` / `async with` does this automatically; if you drive the GATT
  characteristic yourself, send `auth_frame("j")` before any command.
- **Commands seem dropped** — keep ~500 ms between commands; the firmware
  throttles input (`COMMAND_INTERVAL_S`).
