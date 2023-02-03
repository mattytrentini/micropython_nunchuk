# SPDX-FileCopyrightText: 2019 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`nunchuk`
================================================================================

MicroPython library for Nintendo Nunchuk controller


* Author(s): Carter Nelson, Matt Trentini, Oliver Robson

Implementation Notes
--------------------

**Hardware:**

* `Wii Remote Nunchuk <https://en.wikipedia.org/wiki/Wii_Remote#Nunchuk>`_
* `Wiichuck <https://www.adafruit.com/product/342>`_
"""
import time
from collections import namedtuple
from machine import I2C


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/mattytrentini/micropython_nunchuk"


class Nunchuk:
    """Class which provides an interface to a Nintendo Nunchuk controller.

    :param ~I2C i2c: The `machine.I2C` object to use.
    :param int address: (Optional) The I2C address of the device. Default is 0x52.
    :param int i2c_read_delay_us: (Optional) The time in microseconds to pause
        between the I2C write and read. This needs to be at least 200us.
    :param int i2c_init_delay_ms: (Optional) The time in milliseconds to pause
        before each write to unencrypt the Nunchuk communications.
    """

    _Values = namedtuple("Values", ("joystick", "buttons", "acceleration"))
    _Joystick = namedtuple("Joystick", ("x", "y"))
    _Buttons = namedtuple("Buttons", ("C", "Z"))
    _Acceleration = namedtuple("Acceleration", ("x", "y", "z"))

    def __init__(
        self,
        i2c: I2C,
        address: int = 0x52,
        i2c_read_delay_us: int = 200,
        i2c_init_delay_ms: int = 100
    ) -> None:
        self.buffer = bytearray(6)
        self.address = address
        self._i2c = i2c
        self._i2c_read_delay_us = i2c_read_delay_us

        time.sleep_ms(i2c_init_delay_ms)
        # turn off encrypted data
        # http://wiibrew.org/wiki/Wiimote/Extension_Controllers
        self._i2c.writeto(self.address, bytes([0xF0, 0x55]))
        time.sleep_ms(i2c_init_delay_ms)
        self._i2c.writeto(self.address, bytes([0xFB, 0x00]))

    @property
    def values(self) -> _Values:
        """The current state of all values."""
        self._read_data()
        return self._Values(
            self._joystick(do_read=False),
            self._buttons(do_read=False),
            self._acceleration(do_read=False),
        )

    @property
    def joystick(self) -> _Joystick:
        """The current joystick position (from 0 to 255)."""
        return self._joystick()

    @property
    def buttons(self) -> _Buttons:  # pylint: disable=invalid-name
        """The current pressed state of buttons C and Z (boolean)."""
        return self._buttons()

    @property
    def acceleration(self) -> _Acceleration:
        """The current accelerometer reading (from 0 to 512)."""
        return self._acceleration()

    def _joystick(self, do_read: bool = True) -> _Joystick:
        if do_read:
            self._read_data()
        return self._Joystick(self.buffer[0], self.buffer[1])  # x, y

    def _buttons(self, do_read: bool = True) -> _Buttons:
        if do_read:
            self._read_data()
        return self._Buttons(
            not bool(self.buffer[5] & 0x02), not bool(self.buffer[5] & 0x01)  # C  # Z
        )

    def _acceleration(self, do_read: bool = True) -> _Acceleration:
        if do_read:
            self._read_data()
        return self._Acceleration(
            ((self.buffer[5] & 0xC0) >> 6) | (self.buffer[2] << 2),  # ax
            ((self.buffer[5] & 0x30) >> 4) | (self.buffer[3] << 2),  # ay
            ((self.buffer[5] & 0x0C) >> 2) | (self.buffer[4] << 2),  # az
        )

    def _read_data(self) -> bytearray:
        return self._read_register(0x00)

    def _read_register(self, register) -> bytearray:
        self._i2c.writeto(self.address, bytes([register]))
        time.sleep_us(self._i2c_read_delay_us)
        self._i2c.readfrom_into(self.address, self.buffer)
        return self.buffer
