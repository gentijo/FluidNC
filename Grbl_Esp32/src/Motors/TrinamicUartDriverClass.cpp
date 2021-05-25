/*
    TrinamicUartDriverClass.cpp

    This is used for Trinamic UART controlled stepper motor drivers.

    Part of Grbl_ESP32
    2020 -	The Ant Team
    2020 -	Bart Dring

    TMC2209 Datasheet
    https://www.trinamic.com/fileadmin/assets/Products/ICs_Documents/TMC2209_Datasheet_V103.pdf

    Grbl is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    Grbl is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Grbl.  If not, see <http://www.gnu.org/licenses/>.

*/
#include "TrinamicUartDriver.h"
#include "../MachineConfig.h"

#include <TMCStepper.h>
#include <atomic>

Uart tmc_serial(TMC_UART);

namespace Motors {

    bool TrinamicUartDriver::_uart_started = false;

    TrinamicUartDriver* TrinamicUartDriver::List = NULL;  // a static list of all drivers for stallguard reporting

    uint8_t TrinamicUartDriver::get_next_index() {
        static uint8_t index = 1;  // they start at 1
        return index++;
    }

    /* HW Serial Constructor. */
    TrinamicUartDriver::TrinamicUartDriver(uint16_t driver_part_number, uint8_t addr) :
        StandardStepper(), _driver_part_number(driver_part_number), _addr(addr) {}

    void TrinamicUartDriver::init() {
        if (!_uart_started) {
#ifdef LATER
            tmc_serial.setPins(TMC_UART_TX, TMC_UART_RX);
#endif
            tmc_serial.begin(115200, Uart::Data::Bits8, Uart::Stop::Bits1, Uart::Parity::None);
            _uart_started = true;
        }
        _has_errors = hw_serial_init();

        link = List;
        List = this;

        // Display the stepper library version message once, before the first
        // TMC config message.  Link is NULL for the first TMC instance.
        if (!link) {
            grbl_msg_sendf(CLIENT_SERIAL, MsgLevel::Info, "TMCStepper Library Ver. 0x%06x", TMCSTEPPER_VERSION);
        }

        if (_has_errors) {
            return;
        }

        config_message();

        tmcstepper->begin();

        _has_errors = !test();  // Try communicating with motor. Prints an error if there is a problem.

        read_settings();  // pull info from settings
        set_mode(false);

        // After initializing all of the TMC drivers, create a task to
        // display StallGuard data.  List == this for the final instance.
        if (List == this) {
            xTaskCreatePinnedToCore(readSgTask,    // task
                                    "readSgTask",  // name for task
                                    4096,          // size of task stack
                                    NULL,          // parameters
                                    1,             // priority
                                    NULL,
                                    SUPPORT_TASK_CORE  // must run the task on same core
            );
        }
    }

    bool TrinamicUartDriver::hw_serial_init() {
        if (_driver_part_number == 2209) {
            tmcstepper = new TMC2209Stepper(&tmc_serial, _r_sense, _addr);
            return false;
        }
        grbl_msg_sendf(CLIENT_SERIAL, MsgLevel::Info, "Unsupported Trinamic motor p/n:%d", _driver_part_number);
        return true;
    }

    /*
        This is the startup message showing the basic definition. 
    */
    void TrinamicUartDriver::config_message() {  //TODO: The RX/TX pin could be added to the msg.
        grbl_msg_sendf(CLIENT_SERIAL,
                       MsgLevel::Info,
                       "%s motor Trinamic TMC%d Step:%s Dir:%s Disable:%s UART%d Rx:%s Tx:%s Addr:%d R:%0.3f %s",
                       reportAxisNameMsg(axis_index(), dual_axis_index()),
                       _driver_part_number,
                       _step_pin.name().c_str(),
                       _dir_pin.name().c_str(),
                       _disable_pin.name().c_str(),
                       TMC_UART,
#ifdef LATER
                       pinName(TMC_UART_RX),
                       pinName(TMC_UART_TX),
#else
                       0,
                       0,
#endif
                       _addr,
                       _r_sense,
                       reportAxisLimitsMsg(axis_index()));
    }

    bool TrinamicUartDriver::test() {
        if (_has_errors) {
            return false;
        }

        switch (tmcstepper->test_connection()) {
            case 1:
                grbl_msg_sendf(CLIENT_SERIAL,
                               MsgLevel::Info,
                               "%s driver test failed. Check connection",
                               reportAxisNameMsg(axis_index(), dual_axis_index()));
                return false;
            case 2:
                grbl_msg_sendf(CLIENT_SERIAL,
                               MsgLevel::Info,
                               "%s driver test failed. Check motor power",
                               reportAxisNameMsg(axis_index(), dual_axis_index()));
                return false;
            default:
                // driver responded, so check for other errors from the DRV_STATUS register

                TMC2208_n ::DRV_STATUS_t status { 0 };  // a useful struct to access the bits.
                status.sr = tmcstepper->DRV_STATUS();

                bool err = false;

                // look for errors
                if (report_short_to_ground(status)) {
                    err = true;
                }

                if (report_over_temp(status)) {
                    err = true;
                }

                if (report_short_to_ps(status)) {
                    err = true;
                }

                if (err) {
                    return false;
                }

                grbl_msg_sendf(CLIENT_SERIAL, MsgLevel::Info, "%s driver test passed", reportAxisNameMsg(axis_index(), dual_axis_index()));
                return true;
        }
    }

    /*
    Read setting and send them to the driver. Called at init() and whenever related settings change
    both are stored as float Amps, but TMCStepper library expects...
    uint16_t run (mA)
    float hold (as a percentage of run)
    */
    void TrinamicUartDriver::read_settings() {
        if (_has_errors) {
            return;
        }

        uint16_t run_i_ma = (uint16_t)(_run_current * 1000.0);
        float    hold_i_percent;

        if (_run_current == 0) {
            hold_i_percent = 0;
        } else {
            hold_i_percent = _hold_current / _run_current;
            if (hold_i_percent > 1.0)
                hold_i_percent = 1.0;
        }

        tmcstepper->microsteps(_microsteps);
        tmcstepper->rms_current(run_i_ma, hold_i_percent);

        init_step_dir_pins();
    }

    bool TrinamicUartDriver::set_homing_mode(bool isHoming) {
        set_mode(isHoming);
        return true;
    }

    /*
    There are ton of settings. I'll start by grouping then into modes for now.
    Many people will want quiet and stallgaurd homing. Stallguard only run in
    Coolstep mode, so it will need to switch to Coolstep when homing
    */
    void TrinamicUartDriver::set_mode(bool isHoming) {
        if (_has_errors) {
            return;
        }

        TrinamicUartMode newMode = isHoming ? TRINAMIC_UART_HOMING_MODE : TRINAMIC_UART_RUN_MODE;

        if (newMode == _mode) {
            return;
        }
        _mode = newMode;

        switch (_mode) {
            case TrinamicUartMode ::StealthChop:
                //grbl_msg_sendf(CLIENT_SERIAL, MsgLevel::Info, "StealthChop");
                tmcstepper->en_spreadCycle(false);
                tmcstepper->pwm_autoscale(true);
                break;
            case TrinamicUartMode ::CoolStep:
                //grbl_msg_sendf(CLIENT_SERIAL, MsgLevel::Info, "Coolstep");
                // tmcstepper->en_pwm_mode(false); //TODO: check if this is present in TMC2208/09
                tmcstepper->en_spreadCycle(true);
                tmcstepper->pwm_autoscale(false);
                break;
            case TrinamicUartMode ::StallGuard:  //TODO: check all configurations for stallguard
            {
                auto axisConfig     = config->_axes->_axis[this->axis_index()];
                auto homingFeedRate = (axisConfig->_homing != nullptr) ? axisConfig->_homing->_feedRate : 200;
                //grbl_msg_sendf(CLIENT_SERIAL, MsgLevel::Info, "Stallguard");
                tmcstepper->en_spreadCycle(false);
                tmcstepper->pwm_autoscale(false);
                tmcstepper->TCOOLTHRS(calc_tstep(homingFeedRate, 150.0));
                tmcstepper->SGTHRS(constrain(_stallguard, 0, 255));
                break;
            }
            default:
                grbl_msg_sendf(CLIENT_SERIAL, MsgLevel::Info, "Unknown Trinamic mode:d", _mode);
        }
    }

    /*
    This is the stallguard tuning info. It is call debug, so it could be generic across all classes.
    */
    void TrinamicUartDriver::debug_message() {
        if (_has_errors) {
            return;
        }
        uint32_t tstep = tmcstepper->TSTEP();

        if (tstep == 0xFFFFF || tstep < 1) {  // if axis is not moving return
            return;
        }
        float feedrate = st_get_realtime_rate();  //* settings.microsteps[axis_index] / 60.0 ; // convert mm/min to Hz

        grbl_msg_sendf(CLIENT_SERIAL,
                       MsgLevel::Info,
                       "%s SG_Val: %04d   Rate: %05.0f mm/min SG_Setting:%d",
                       reportAxisNameMsg(axis_index(), dual_axis_index()),
                       tmcstepper->SG_RESULT(),  //    tmcstepper->sg_result(),
                       feedrate,
                       constrain(_stallguard, -64, 63));

        TMC2208_n ::DRV_STATUS_t status { 0 };  // a useful struct to access the bits.
        status.sr = tmcstepper->DRV_STATUS();

        // these only report if there is a fault condition
        report_open_load(status);
        report_short_to_ground(status);
        report_over_temp(status);
        report_short_to_ps(status);

        // grbl_msg_sendf(CLIENT_SERIAL,
        //                MsgLevel::Info,
        //                "%s Status Register %08x GSTAT %02x",
        //                reportAxisNameMsg(axis_index(), dual_axis_index()),
        //                status.sr,
        //                tmcstepper->GSTAT());
    }

    // calculate a tstep from a rate
    // tstep = TRINAMIC_UART_FCLK / (time between 1/256 steps)
    // This is used to set the stallguard window from the homing speed.
    // The percent is the offset on the window
    uint32_t TrinamicUartDriver::calc_tstep(float speed, float percent) {
        double tstep = speed / 60.0 * config->_axes->_axis[axis_index()]->_stepsPerMm * (256.0 / _microsteps);
        tstep        = TRINAMIC_UART_FCLK / tstep * percent / 100.0;

        return static_cast<uint32_t>(tstep);
    }

    // this can use the enable feature over SPI. The dedicated pin must be in the enable mode,
    // but that can be hardwired that way.
    void TrinamicUartDriver::set_disable(bool disable) {
        if (_has_errors) {
            return;
        }

        if (_disabled == disable) {
            return;
        }

        _disabled = disable;

        _disable_pin.write(_disabled);

#ifdef USE_TRINAMIC_ENABLE
        if (_disabled) {
            tmcstepper->toff(TRINAMIC_UART_TOFF_DISABLE);
        } else {
            if (_mode == TrinamicUartMode::StealthChop) {
                tmcstepper->toff(TRINAMIC_UART_TOFF_STEALTHCHOP);
            } else {
                tmcstepper->toff(TRINAMIC_UART_TOFF_COOLSTEP);
            }
        }
#endif
        // the pin based enable could be added here.
        // This would be for individual motors, not the single pin for all motors.
    }

    // Prints StallGuard data that is useful for tuning.
    void TrinamicUartDriver::readSgTask(void* pvParameters) {
        TickType_t       xLastWakeTime;
        const TickType_t xreadSg = 200;  // in ticks (typically ms)
        auto             n_axis  = config->_axes->_numberAxis;

        xLastWakeTime = xTaskGetTickCount();  // Initialise the xLastWakeTime variable with the current time.
        while (true) {                        // don't ever return from this or the task dies
            std::atomic_thread_fence(std::memory_order::memory_order_seq_cst);  // read fence for settings
            if (sys.state == State::Cycle || sys.state == State::Homing || sys.state == State::Jog) {
                for (TrinamicUartDriver* p = List; p; p = p->link) {
                    if (p->_stallguardDebugMode) {
                        //grbl_msg_sendf(CLIENT_SERIAL, MsgLevel::Info, "SG:%d", _stallguardDebugMode);
                        p->debug_message();
                    }
                }
            }  // sys.state

            vTaskDelayUntil(&xLastWakeTime, xreadSg);

            static UBaseType_t uxHighWaterMark = 0;
#ifdef DEBUG_TASK_STACK
            reportTaskStackSize(uxHighWaterMark);
#endif
        }
    }

    // =========== Reporting functions ========================

    bool TrinamicUartDriver::report_open_load(TMC2208_n ::DRV_STATUS_t status) {
        if (status.ola || status.olb) {
            grbl_msg_sendf(CLIENT_SERIAL,
                           MsgLevel::Info,
                           "%s Driver Open Load a:%s b:%s",
                           reportAxisNameMsg(axis_index(), dual_axis_index()),
                           status.ola ? "Y" : "N",
                           status.olb ? "Y" : "N");
            return true;
        }
        return false;  // no error
    }

    bool TrinamicUartDriver::report_short_to_ground(TMC2208_n ::DRV_STATUS_t status) {
        if (status.s2ga || status.s2gb) {
            grbl_msg_sendf(CLIENT_SERIAL,
                           MsgLevel::Info,
                           "%s Driver Short Coil a:%s b:%s",
                           reportAxisNameMsg(axis_index(), dual_axis_index()),
                           status.s2ga ? "Y" : "N",
                           status.s2gb ? "Y" : "N");
            return true;
        }
        return false;  // no error
    }

    bool TrinamicUartDriver::report_over_temp(TMC2208_n ::DRV_STATUS_t status) {
        if (status.ot || status.otpw) {
            grbl_msg_sendf(CLIENT_SERIAL,
                           MsgLevel::Info,
                           "%s Driver Temp Warning:%s Fault:%s",
                           reportAxisNameMsg(axis_index(), dual_axis_index()),
                           status.otpw ? "Y" : "N",
                           status.ot ? "Y" : "N");
            return true;
        }
        return false;  // no error
    }

    bool TrinamicUartDriver::report_short_to_ps(TMC2208_n ::DRV_STATUS_t status) {
        // check for short to power supply
        if ((status.sr & bit(12)) || (status.sr & bit(13))) {
            grbl_msg_sendf(CLIENT_SERIAL,
                           MsgLevel::Info,
                           "%s Driver Short vsa:%s vsb:%s",
                           reportAxisNameMsg(axis_index(), dual_axis_index()),
                           (status.sr & bit(12)) ? "Y" : "N",
                           (status.sr & bit(13)) ? "Y" : "N");
            return true;
        }
        return false;  // no error
    }

    // Configuration registration
    namespace {
        MotorFactory::InstanceBuilder<TMC2008> registration_2008("tmc_2008");
        MotorFactory::InstanceBuilder<TMC2009> registration_2009("tmc_2009");
    }
}
