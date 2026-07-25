# Apitor robots & their motor mappings

This is a **reference** table of the buildable models in each Apitor BLE kit and the exact motor directions the **official app** sends for forward / backward / turn-right / turn-left. It was extracted from the app's `robot_config/<product>/all_robot_config.json` assets (joystick leaf 0 = forward, 4 = right, 8 = backward, 12 = left).

> These are the values for each **official build**. If you built the model differently, or plugged the motors into different ports, your robot may need different settings — that's what the calibration steps in [EASY.md](EASY.md#setting-up-a-different-robot) are for. Direction `D1`/`D2` are the two spin directions; the number after `/` is the speed (1-12).

Driving always uses **motor 1 and motor 2** (the wheels). Motor 3, when present, drives an accessory (a drill, a launcher arm, a crane) and is not part of driving.


## Robot J  (`product="j"`)

7 buildable model(s) in this kit.

| # | Model | Forward | Backward | Turn right | Turn left | Easy-mode wheels | Kind |
|--:|-------|---------|----------|-----------|-----------|------------------|------|
| 0 | (common) | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M2(D1 fwd) right=M1(D2 fwd) | drivable |
| 1 | Drill Car | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M2(D1 fwd) right=M1(D2 fwd) | drivable |
| 2 | Robot J | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 3 | Tank | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 4 | Mars Rover | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M2(D1 fwd) right=M1(D2 fwd) | drivable |
| 5 | Robo Car | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 6 | Launcher | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M2(D1 fwd) right=M1(D2 fwd) | drivable |

## Robot S  (`product="s"`)

11 buildable model(s) in this kit.

| # | Model | Forward | Backward | Turn right | Turn left | Easy-mode wheels | Kind |
|--:|-------|---------|----------|-----------|-----------|------------------|------|
| 0 | (common) | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 1 | RC Car | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 2 | Elephant | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M2(D1 fwd) right=M1(D2 fwd) | drivable |
| 3 | Merry-Go-Round | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 4 | Crane | M1:D1/12 M2:D2/1 | M1:D2/12 M2:D1/1 | M1:D1/12 M2:D1/1 | M1:D2/12 M2:D2/1 | — | steering build (one slow motor) |
| 5 | Music Box | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 6 | Mystery Box | M1:D1/12 M2:D2/12 | M1:D1/12 M2:D2/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 7 | Robot Vacuum | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 8 | Pendulum Ride | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 9 | Airplane | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M2(D1 fwd) right=M1(D2 fwd) | drivable |
| 10 | Boxer | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |

## Robot Q  (`product="q"`)

19 buildable model(s) in this kit.

| # | Model | Forward | Backward | Turn right | Turn left | Easy-mode wheels | Kind |
|--:|-------|---------|----------|-----------|-----------|------------------|------|
| 0 | (common) | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 1 | Gorilla | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 2 | Locomotive | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M2(D2 fwd) right=M1(D1 fwd) | drivable |
| 3 | Racing Car | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 4 | Rowing | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 5 | Spinning Top | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 6 | Dog | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 7 | Tower Crane | M1:D1/12 M2:D1/1 | M1:D2/12 M2:D2/1 | M1:D1/12 M2:D2/1 | M1:D2/12 M2:D1/1 | — | steering build (one slow motor) |
| 8 | Motorcycle | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 9 | Rocking Boat | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 10 | Golf | M1:D2/12 M2:D1/12 | M1:D2/12 M2:D1/12 | M1:D2/12 M2:D1/12 | M1:D2/12 M2:D1/12 | — | not drivable (fixed motion) |
| 11 | Basketball Machine | M1:D2/12 M2:D1/12 | M1:D2/12 M2:D1/12 | M1:D2/12 M2:D1/12 | M1:D2/12 M2:D1/12 | — | not drivable (fixed motion) |
| 12 | Swing | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 13 | Seesaw | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 14 | Horizontal Bar | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 15 | Automatic Door | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 16 | Clown | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 17 | Dancing | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 18 | Detection Vehicle | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |

## Robot R  (`product="r"`)

5 buildable model(s) in this kit.

| # | Model | Forward | Backward | Turn right | Turn left | Easy-mode wheels | Kind |
|--:|-------|---------|----------|-----------|-----------|------------------|------|
| 0 | (common) | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 1 | Off-Roader | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 2 | Rocket Car | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 3 | Pickup | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 4 | Robo Bug | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M2(D1 fwd) right=M1(D2 fwd) | drivable |

## Robot X  (`product="x"`)

13 buildable model(s) in this kit.

| # | Model | Forward | Backward | Turn right | Turn left | Easy-mode wheels | Kind |
|--:|-------|---------|----------|-----------|-----------|------------------|------|
| 0 | (common) | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 1 | Racing Car | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 2 | Digital Piano | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 3 | Robot X | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M2(D2 fwd) right=M1(D1 fwd) | drivable |
| 4 | Tuk-Tuk | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 5 | Violin | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 6 | Dinosaur | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 7 | Helicopter | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 8 | Catapult | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M2(D2 fwd) right=M1(D1 fwd) | drivable |
| 9 | Monster | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 10 | Drawing Machine | M1:D1/1 M2:D1/5 | M1:D1/1 M2:D1/5 | M1:D1/1 M2:D1/5 | M1:D1/1 M2:D1/5 | — | not drivable (fixed motion) |
| 11 | Lifter | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D1/12 | M1:D2/12 M2:D2/12 | left=M1(D1 fwd) right=M2(D2 fwd) | drivable |
| 12 | Color Sorter | M1:D2/12 M2:D1/12 | M1:D1/12 M2:D2/12 | M1:D2/12 M2:D2/12 | M1:D1/12 M2:D1/12 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |

## Wheels  (`product="w"`)

5 buildable model(s) in this kit.

| # | Model | Forward | Backward | Turn right | Turn left | Easy-mode wheels | Kind |
|--:|-------|---------|----------|-----------|-----------|------------------|------|
| 0 | (common) | M1:D2/10 M2:D1/10 | M1:D1/10 M2:D2/10 | M1:D2/10 M2:D2/10 | M1:D1/10 M2:D1/10 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 1 | Racing Car | M1:D2/10 M2:D1/10 | M1:D1/10 M2:D2/10 | M1:D2/10 M2:D2/10 | M1:D1/10 M2:D1/10 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 2 | Digital Piano | M1:D2/10 M2:D1/10 | M1:D1/10 M2:D2/10 | M1:D2/10 M2:D2/10 | M1:D1/10 M2:D1/10 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 3 | Robot X | M1:D2/10 M2:D1/10 | M1:D1/10 M2:D2/10 | M1:D2/10 M2:D2/10 | M1:D1/10 M2:D1/10 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |
| 4 | Tuk-Tuk | M1:D2/10 M2:D1/10 | M1:D1/10 M2:D2/10 | M1:D2/10 M2:D2/10 | M1:D1/10 M2:D1/10 | left=M1(D2 fwd) right=M2(D1 fwd) | drivable |

## How to read the "Easy-mode wheels" column

For drivable models this library models the robot as a left wheel and a right wheel. The column tells you which motor port is which wheel, and which spin direction (`D1`/`D2`) moves that wheel forward. You can pass those straight to the easy API, e.g. for a build whose right wheel is motor 1 spinning `D2` and left wheel is motor 2 spinning `D1`:

```python
from apitor_ble.easy import Robot
from apitor_ble.protocol import Motor, Direction
from apitor_ble.profiles import RobotProfile

profile = RobotProfile(
    product="j", name="My Drill Car",
    left_motor=Motor.M2, left_forward=Direction.D1,
    right_motor=Motor.M1, right_forward=Direction.D2,
    calibrated=True,
)
robot = Robot(profile=profile)
```

If you'd rather not think about any of this, just use the calibration steps in [EASY.md](EASY.md#setting-up-a-different-robot) — you watch the robot and flip a couple of switches until forward is forward.

