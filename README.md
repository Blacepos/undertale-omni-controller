# Undertale Omnidirectional Controller
A script which translates gamepad joystick input into keypresses. Undertale normally works with a gamepad, but the player is locked into 8 directions. For example, if I hold the stick to the right and slightly up, the player will only move to the right. This script attempts to allow the player to move in any direction by precisely tapping direction keys.

The script tracks the right stick since the left stick already used.

## Usage

It is recommended to use the v2 script since it's just better.

### Prerequisites

[Python](https://www.python.org/) must be installed with the [`keyboard`](https://pypi.org/project/keyboard/) and [`inputs`](https://pypi.org/project/inputs/) modules

### Running

```sh
python3 undertale_omni_controller_v2.py
```

Use Ctrl+C to terminate.

It is recommended to move the joystick around on startup so the script can learn the limits for each axis.