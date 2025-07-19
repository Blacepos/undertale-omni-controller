# Undertale Omnidirectional Controller
A barely usable script which translates controller joystick input into keypresses. Undertale normally works with a controller, but the player is locked into 8 directions. For example, if I hold the stick to the right and slightly up, the player will only move to the right. This script attempts to allow the player to move in any direction by precisely tapping direction keys.

The script tracks the right stick since the left stick is the one Undertale is already reading.

## Usage

It is recommended to use the v2 script since it's just better.

### Prerequisites

[Python](https://www.python.org/) must be installed with the [`keyboard`](https://pypi.org/project/keyboard/) and [`inputs`](https://pypi.org/project/inputs/) modules

### Running

```sh
python3 undertale_omni_controller_v2.py
```