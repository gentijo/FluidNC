from MotorDriver import MotorDriver

class Nullmotor(MotorDriver):

    def __init__(self, name:str) -> None:
        self._name = name;
    
    def set_homing_mode(self, isHoming:bool) -> bool:
        return False

    def isReal(self) -> bool:
        return False
    
    # // Configuration handlers:
    def group(self, handler:handlerBase):
        pass