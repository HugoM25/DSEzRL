import time 
import multiprocessing
from desmume.emulator import DeSmuME
from desmume.controls import keymask, Keys


class DSInstance : 
    def __init__(self, rom_path: str, auto_run: bool, fps: int, request_queue: multiprocessing.Queue, response_queue: multiprocessing.Queue):
        self.rom_path = rom_path
        self.auto_run = auto_run
        self.fps = fps
        self.request_queue = request_queue
        self.response_queue = response_queue

    def run_emulator(self) -> None:
        '''
        Run the emulator in a separate process

        Returns:
            None
        '''

        self.emu = DeSmuME()
        self.emu.open(self.rom_path)
        window = self.emu.create_sdl_window()

        self.emu.volume_set(0)

        while not window.has_quit():
            window.process_input()
            # Handle commands (if any)
            if not self.request_queue.empty() :
                # Get the command
                command_id, command = self.request_queue.get()    

                response = None
                # print(f"Command of type {command.command_type} received")
                # Execute the command
                if command.command_type == 'screenshot_cmd':
                    response = self.emu.screenshot()
                elif command.command_type == 'load_savestate_cmd' : 
                    self.emu.savestate.load_file(command.path_to_savestate)
                elif command.command_type == 'read_memory_cmd' :
                    response = self.read_memory(command)
                elif command.command_type == 'set_inputs' :
                    response = self.handle_inputs(command)
                    if self.auto_run == False : 
                        self.do_cycles(10)
                elif command.command_type == 'do_cycles' :
                    self.do_cycles(command.cycles_count)

                # Send the response
                self.response_queue.put((command_id, response))
        
            # If auto_run is True, run the emulator
            if self.auto_run:
                self.emu.cycle()
                time.sleep(1/self.fps)  # 60 FPS    

            window.draw()
    
    def do_cycles(self, cycles_count) :
        for _ in range(0, cycles_count) : 
            self.emu.cycle()

    def read_memory(self, command) : 
        response = []
        ds_memory = self.emu.memory
        unsigned = ds_memory.unsigned
        signed = ds_memory.signed

        for i in range(0, len(command.memory_addr)) : 
            addr = command.memory_addr[i]
            if command.memory_addr_types[i] == 'u_byte' : 
                response.append((addr, unsigned.read_byte(addr))) 
            elif command.memory_addr_types[i] == 'u_short' : 
                response.append((addr, unsigned.read_short(addr))) 
            elif command.memory_addr_types[i] == 'u_long' : 
                response.append((addr, unsigned.read_long(addr)))   
            elif command.memory_addr_types[i] == 's_byte' : 
                response.append((addr, signed.read_byte(addr))) 
            elif command.memory_addr_types[i] == 's_short' : 
                response.append((addr, signed.read_short(addr))) 
            elif command.memory_addr_types[i] == 's_long' : 
                response.append((addr, signed.read_long(addr)))   
        
        return response

    def handle_inputs(self, command) :
        response = None
        ds_inputs = self.emu.input
        # For all the keys
        instructions = command.inputs.to_instructions()
        for instruction in instructions : 
            if instruction[1] :
                self.emu.input.keypad_add_key(keymask(instruction[0]))
            else : 
                self.emu.input.keypad_rm_key(keymask(instruction[0]))
        
        # For touchscreen 
        if command.inputs.touch[2] == False : 
            ds_inputs.touch_release()
        else : 
            ds_inputs.touch_set_pos(command.inputs.touch[0], command.inputs.touch[1])

        return response 
