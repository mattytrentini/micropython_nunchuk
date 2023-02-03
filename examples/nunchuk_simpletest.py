# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
from machine import I2C
import nunchuk

i2c = I2C(1)
print("Scan results: {}".format(i2c.scan()))
nc = nunchuk.Nunchuk(i2c)

while True:
    x, y = nc.joystick
    ax, ay, az = nc.acceleration
    print("joystick = {},{}".format(x, y))
    print("accceleration ax={}, ay={}, az={}".format(ax, ay, az))

    if nc.buttons.C:
        print("button C")
    if nc.buttons.Z:
        print("button Z")
    time.sleep(0.5)
