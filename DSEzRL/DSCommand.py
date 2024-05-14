import time
import random

from .DSInputs import DSInputs

class DSCommand: 
    DEFAULT_COMMAND_CODE = "log"
    def __init__(self, target_instance_index: int = 0, command_type: str = DEFAULT_COMMAND_CODE) -> None:
        self.command_type = command_type
        self.target_instance_index = target_instance_index

        self.generate_command_id()
    
    def generate_command_id(self) -> str : 
        self.command_id = time.time() + random.randint(0, 1000) + self.target_instance_index
        return self.command_id
    
    def set_target_instance(self, new_target_instance_id) -> None :
        self.target_instance_index = new_target_instance_id
        self.generate_command_id()

class ScreenShotCmd(DSCommand) :
    def __init__(self, target_instance_index: int = 0) -> None:
        super().__init__(target_instance_index, "screenshot_cmd") 

class LoadSavestateCmd(DSCommand) : 
    def __init__(self, target_instance_index: int = 0, path_to_savestate: str = "") -> None:
        super().__init__(target_instance_index, "load_savestate_cmd")
        self.path_to_savestate = path_to_savestate

class ReadMemoryCmd(DSCommand) :
    def __init__(self, target_instance_index: int = 0, memory_addr: int = [], memory_addr_types : str = []) -> None:
        super().__init__(target_instance_index, "read_memory_cmd") 
        self.memory_addr = memory_addr
        self.memory_addr_types = memory_addr_types

class SetInputsCmd(DSCommand) : 
    def __init__(self, target_instance_index: int = 0, inputs : DSInputs = None) -> None:
        super().__init__(target_instance_index, "set_inputs")
        self.inputs = inputs

class DoCyclesCmd(DSCommand) :
    def __init__(self, target_instance_index: int = 0, cycles_count : int = 0) -> None:
        super().__init__(target_instance_index, "do_cycles")
        self.cycles_count = cycles_count