#// Copyright (c) 2021 -  Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.


#class PinAttributes:

# Pin capabilities are what a pin _can_ do using the internal hardware. For GPIO pins, these
#are the internal hardware capabilities of the pins, such as the capability to pull-up from
#hardware, wether or not a pin supports input/output, etc.

class PinCapabilities:

    modes = [
        {"None": 0},      # Nonexistent pin
        {"Reserved":1<<1},   # Pin reserved for system use
        {"Input": 1<<2},      # NOTE: Mapped in PinAttributes!
        {"Output":1<<3},     # NOTE: Mapped in PinAttributes!
        {"PullUp":1<<4},    # NOTE: Mapped in PinAttributes!
        {"PullDown", 1<<5},     # NOTE: Mapped in PinAttributes!
        {"ISR": 1<<6},         # NOTE: Mapped in PinAttributes!

        #Other capabilities:
        {"ADC": 1<<7},
        {"DAC": 1<<8},
        {"PWM": 1<<9},
        {"UART",1<<10},

        #// Each class of pins (e.g. GPIO, etc) should have their own 'capability'. This ensures that we
        #// can compare classes of pins along with their properties by just looking at the capabilities.
        {"Native",1<<11},
        {"I2S", 1<<12},
        {"UARTIO", 1<<13},
        {"Error", 1<<14},
        {"Void", 1<<15},
    ]


    def __init__(self, value:int):
        self._value:int = value
 
    def assign(self, capabilities:PinCapabilities):
        self._value = capabilities._value


    def __or__(self, rhs:PinCapabilities) -> PinCapabilities:
        self._value = self._value | rhs._value

    def __and__(self, rhs:PinCapabilities) -> PinCapabilities:
        self._value = self._value & rhs._value

    def __eq_(self, rhs:PinCapabilities) -> PinCapabilities:
        return self._value == rhs._value

    def __ne_(self, rhs:PinCapabilities) -> PinCapabilities:
        return self._value != rhs._value

#        inline operator bool() { return _value != 0; }

#        inline bool has(PinCapabilities t) { return (*this & t) == t; }
 