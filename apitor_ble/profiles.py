"""Per-robot setup for the beginner :mod:`apitor_ble.easy` API.

The low-level protocol (auth handshake, motor frames, LED frames) is the *same*
for every Apitor BLE product — only the authorization key and the advertised
name prefix change, and those are already handled by ``product=`` in
:class:`apitor_ble.ApitorRobot`.

What actually differs from robot to robot in *easy mode* is how you **drive**:
which motor ports are the left and right wheels, and which electrical direction
counts as "forward". That depends on how the kit was physically built, so this
module captures it as a small, overridable :class:`RobotProfile`.

Robot **J** is verified on real hardware (``calibrated=True``). The other
products use reasonable defaults that an educator can calibrate for their own
build — see ``docs/EASY.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from .protocol import Direction, Motor

# Friendly motor number (1/2/3) -> real motor port.
_MOTOR_BY_NUMBER = {1: Motor.M1, 2: Motor.M2, 3: Motor.M3}


def motor_from_number(number: int) -> Motor:
    """Turn a motor number (1, 2, or 3) into the real motor port."""
    if number not in _MOTOR_BY_NUMBER:
        raise ValueError("Motor number must be 1, 2, or 3.")
    return _MOTOR_BY_NUMBER[number]


def opposite(direction: Direction) -> Direction:
    """The other spin direction (D1 <-> D2). STOP stays STOP."""
    if direction is Direction.D1:
        return Direction.D2
    if direction is Direction.D2:
        return Direction.D1
    return Direction.STOP


@dataclass(frozen=True)
class RobotProfile:
    """How one Apitor robot drives in easy mode.

    Attributes
    ----------
    product:
        Single product letter used for the auth key and name filter
        (``"j"``, ``"s"``, ``"q"``, ``"r"``, ``"x"``, ``"w"``).
    name:
        Human-friendly name, e.g. ``"Robot J"``.
    left_motor / right_motor:
        Which motor ports drive the left and right wheels.
    left_forward / right_forward:
        The direction (``D1`` or ``D2``) that moves each wheel *forward*.
    calibrated:
        ``True`` only for mappings verified on real hardware. ``False`` means
        "reasonable guess — please check the driving directions".
    """

    product: str
    name: str
    left_motor: Motor = Motor.M1
    right_motor: Motor = Motor.M2
    left_forward: Direction = Direction.D1
    right_forward: Direction = Direction.D1
    calibrated: bool = False

    def with_overrides(
        self,
        *,
        left_motor: int | None = None,
        right_motor: int | None = None,
        flip_left: bool = False,
        flip_right: bool = False,
    ) -> "RobotProfile":
        """Return a copy adjusted for a specific build.

        ``left_motor``/``right_motor`` reassign the wheels (motor numbers 1-3);
        ``flip_left``/``flip_right`` reverse a wheel whose "forward" goes the
        wrong way. Any override marks the profile as calibrated-by-you.
        """
        changed = False
        lm = self.left_motor
        rm = self.right_motor
        lf = self.left_forward
        rf = self.right_forward
        if left_motor is not None:
            lm = motor_from_number(left_motor)
            changed = True
        if right_motor is not None:
            rm = motor_from_number(right_motor)
            changed = True
        if flip_left:
            lf = opposite(lf)
            changed = True
        if flip_right:
            rf = opposite(rf)
            changed = True
        return replace(
            self,
            left_motor=lm,
            right_motor=rm,
            left_forward=lf,
            right_forward=rf,
            calibrated=self.calibrated or changed,
        )


def drive_directions(
    profile: RobotProfile, forward_left: bool, forward_right: bool
) -> tuple[Motor, Direction, Motor, Direction]:
    """Work out the motor commands for a driving move.

    Returns ``(left_motor, left_dir, right_motor, right_dir)``. ``forward_left``
    / ``forward_right`` say whether each wheel should turn in its forward
    direction (used to build forward/backward/turn moves).
    """
    d_left = profile.left_forward if forward_left else opposite(profile.left_forward)
    d_right = profile.right_forward if forward_right else opposite(profile.right_forward)
    return (profile.left_motor, d_left, profile.right_motor, d_right)


# The known BLE products. Defaults are the *standard build* motor mapping taken
# from the official app's own config (robot_config/<product>/all_robot_config.json,
# model 0). See docs/ROBOTS.md for every buildable model. Only Robot J is
# verified on real hardware (`calibrated=True`); the rest are the official
# values but should still be checked against your build with the calibration
# steps in docs/EASY.md.
PROFILES: dict[str, RobotProfile] = {
    # forward = M1:D2, M2:D1  (turn-right spins both D1)
    "j": RobotProfile(
        "j", "Robot J",
        left_motor=Motor.M2, left_forward=Direction.D1,
        right_motor=Motor.M1, right_forward=Direction.D2,
        calibrated=True,
    ),
    # forward = M1:D2, M2:D1  (turn-right keeps M1 at D2)
    "s": RobotProfile(
        "s", "Robot S",
        left_motor=Motor.M1, left_forward=Direction.D2,
        right_motor=Motor.M2, right_forward=Direction.D1,
    ),
    "q": RobotProfile(
        "q", "Robot Q",
        left_motor=Motor.M1, left_forward=Direction.D2,
        right_motor=Motor.M2, right_forward=Direction.D1,
    ),
    # forward = M1:D1, M2:D2
    "r": RobotProfile(
        "r", "Robot R",
        left_motor=Motor.M1, left_forward=Direction.D1,
        right_motor=Motor.M2, right_forward=Direction.D2,
    ),
    "x": RobotProfile(
        "x", "Robot X",
        left_motor=Motor.M1, left_forward=Direction.D2,
        right_motor=Motor.M2, right_forward=Direction.D1,
    ),
    "w": RobotProfile(
        "w", "Wheels",
        left_motor=Motor.M1, left_forward=Direction.D2,
        right_motor=Motor.M2, right_forward=Direction.D1,
    ),
}


def get_profile(product: str) -> RobotProfile:
    """Look up the built-in profile for a product letter (e.g. ``"j"``)."""
    key = str(product).strip().lower()
    if key not in PROFILES:
        supported = ", ".join(f"'{k}' ({v.name})" for k, v in PROFILES.items())
        raise ValueError(
            f"I don't have a robot called '{product}'. Supported robots: {supported}."
        )
    return PROFILES[key]
