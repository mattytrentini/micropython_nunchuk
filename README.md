# micropython_nunchuk

A MicroPython module for interfacing with Nintendo Nunchuk controllers.

Allows for reading of:

- Joystick position
- Button states
- Accelerometer state

## Installation

Use `mip` (see MicroPython [Package management](https://docs.micropython.org/en/latest/reference/packages.html)):

```bash
> mpremote mip install github:mattytrentini/micropython_nunchuk
```

## Example

See `examples/nunchuk_simpletest.py`. 

Full example:

```bash
> mpremote mount . run examples/nunchuk_simpletest.py
Local directory . is mounted at /remote
Scan results: [82]
joystick = 128,128
accceleration ax=292, ay=527, az=584
joystick = 128,128
```
