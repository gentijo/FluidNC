# Copyright (c) 2020 -	Bart Dring
# Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.


#    TODO
#        Make sure public/private/protected is cleaned up.
#        Only a few Unipolar axes have been setup in init()
#        Get rid of Z_SERVO, just reply on Z_SERVO_PIN
#        Class is ready to deal with non SPI pins, but they have not been needed yet.
#            It would be nice in the config message though
#    Testing
#        Done (success)
#            3 Axis (3 Standard Steppers)
#            MPCNC (dual-motor axis with shared direction pin)
#            TMC2130 Pen Laser (trinamics, stallguard tuning)
#            Unipolar
#        TODO
#            4 Axis SPI (Daisy Chain, dual-motor axis with unique direction pins)
#    Reference
#        TMC2130 Datasheet https://www.trinamic.com/fileadmin/assets/Products/ICs_Documents/TMC2130_datasheet.pdf
#*/

class MotorDriver():

    MAX_N_AXIS=10

    def __init__(self, _name:str):
        self.name:str =_name
        self.max_n_axis:int = MAX_N_AXIS;
        self.axis_mask:int  = (1 << self.max_n_axis) - 1;
        pass;
    
    def axisName(self):
        return config->_axes->axisName(axis_index())) + (dual_axis_index() ? "2" : "") + " Axis";
    

    def debug_message(self):
        pass

    def test(self):
        return True # true = OK

    size_t MotorDriver::axis_index() const {
        Assert(config != nullptr && config->_axes != nullptr, "Expected machine to be configured before this is called.");
        return size_t(config->_axes->findAxisIndex(this));
    }
    size_t MotorDriver::dual_axis_index() const {
        Assert(config != nullptr && config->_axes != nullptr, "Expected machine to be configured before this is called.");
        return size_t(config->_axes->findAxisMotor(this));
    }

    def read_settings(self) -> None:
        return None;

    # set_homing_mode() is called from motors_set_homing_mode(),
    # which in turn is called at the beginning of a homing cycle
    # with isHoming true, and at the end with isHoming false.
    # Some motor types require differ setups for homing and
    # normal operation.  Returns true if the motor can home
    def set_homing_mode(self, isHoming:bool) ->bool:
        return False;
    

    # set_disable() disables or enables a motor.  It is used to
    # make a motor transition between idle and non-idle states.
    def set_disable(self, disable:bool) -> None:
        pass

    # set_direction() sets the motor movement direction.  It is
    # invoked for every motion segment.
    def set_direction(_dir:bool) ->None:
        pass

    # step() initiates a step operation on a motor.  It is called
    # from motors_step() for ever motor than needs to step now.
    # For ordinary step/direction motors, it sets the step pin
    # to the active state.
    def step(self) -> None:
        pass


    # unstep() turns off the step pin, if applicable, for a motor.
    # It is called from motors_unstep() for all motors, since
    # motors_unstep() is used in many contexts where the previous
    # states of the step pins are unknown.
    def unstep(self) -> None;

    # this is used to configure and test motors. This would be used for Trinamic
    def config_motor(self) -> None:
        pass

    # test(), called from init(), checks to see if a motor is
    # responsive, returning true on failure.  Typical
    # implementations also display messages to show the result.
    # TODO Architecture: Should this be private?
    def test(self) -> bool:
        pass

    # Name is required for the configuration factory to work.
    def name(self) -> str: 
        return self._name
    

    # Test for a real motor as opposed to a NullMotor placeholder
    def isReal(self) -> bool:
        return True

        // Virtual base classes require a virtual destructor.
        virtual ~MotorDriver() {}

    def axisName(self) -> str:
        return ""
    
    # config_message(), called from init(), displays a message describing
    # the motor configuration - pins and other motor-specific items
    def config_message(self) -> None:
        pass

    # _axis_index is the axis from XYZABC, while
    # _dual_axis_index is 0 for the first motor on that
    # axis and 1 for the second motor.
    # These variables are used for several purposes:
    # * Displaying the axis name in messages
    # * When reading settings, determining which setting
    #   applies to this motor
    # * For some motor types, it is necessary to maintain
    #   tables of all the motors of that type; those
    #   tables can be indexed by these variables.
    # TODO Architecture: It might be useful to cache a
    # reference to the axis settings entry.

    def axis_index(self) -> int:
        pass  #// X_AXIS, etc
        size_t dual_axis_index() const;  // motor number 0 or 1
