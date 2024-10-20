from MotorDriver import MotorDriver

class StandardStepper(MotorDriver):

    # //StandardStepper(size_t axis_index, Pin step_pin, Pin dir_pin, Pin disable_pin);

    def __init__(self, name:str):
        self._name = name;
        self.step_pin:Pin = None
        self.dir_pin:Pin = None
        self._disable_pin = None
        self._invert_step:bool = None
        self._invert_disable:bool = None
        #rmt_channel_t _rmt_chan_num = RMT_CHANNEL_MAX;
    #// Initialized after configuration for RMT steps:



    #// Overrides for inherited methods
    def set_homing_mode(self, isHoming:bool) -> bool:
        return True

    def init_step_dir_pins(self) -> None:
        pass

    def config_message(self) -> None:
        pass

    #// Configuration handlers:
    def validate(self):
        pass

    def group( self, Configuration::HandlerBase handler):
        handler.item("step_pin", _step_pin)
        handler.item("direction_pin", _dir_pin)
        handler.item("disable_pin", _disable_pin)
    
