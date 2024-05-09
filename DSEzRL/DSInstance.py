import time 
import multiprocessing
from desmume.emulator import DeSmuME
from desmume.controls import keymask, Keys

class DSInstance:
    @staticmethod
    def run_emulator(rom_path: str, auto_run: bool, fps: int, request_queue: multiprocessing.Queue, response_queue: multiprocessing.Queue) -> None:
        '''
        Run the emulator in a separate process
        
        Args:
            rom_path (str): Path to the ROM
            auto_run (bool): If True, the emulator will run automatically else it will wait for commands
            fps (int): Number of frames per second
            request_queue (multiprocessing.Queue): Queue to receive commands
            response_queue (multiprocessing.Queue): Queue to send responses

        Returns:
            None
        '''

        emu = DeSmuME()
        emu.open(rom_path)
        window = emu.create_sdl_window()

        emu.volume_set(0)

        while not window.has_quit():
            window.process_input()
            # Handle commands (if any)
            if not request_queue.empty() :
                # Get the command
                command_id, command = request_queue.get()    
            
                response = None
                # print(f"Command of type {command.command_type} received")
                # Execute the command
                if command.command_type == 'screenshot_cmd':
                    response = emu.screenshot()
                elif command.command_type == 'load_savestate_cmd' : 
                    emu.savestate.load_file(command.path_to_savestate)
                elif command.command_type == 'read_memory_cmd' :
                    response = []
                    ds_memory = emu.memory
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

                elif command.command_type == 'set_inputs' :
                    ds_inputs = emu.input
                    # For all the keys
                    instructions = command.inputs.to_instructions()
                    for instruction in instructions : 
                        if instruction[1] :
                            emu.input.keypad_add_key(keymask(instruction[0]))
                        else : 
                            emu.input.keypad_rm_key(keymask(instruction[0]))
                    
                    # For touchscreen 
                    if command.inputs.touch[2] == False : 
                        ds_inputs.touch_release()
                    else : 
                        ds_inputs.touch_set_pos(command.inputs.touch[0], command.inputs.touch[1])


                # Send the response
                response_queue.put((command_id, response))

            if auto_run:
                emu.cycle()
                time.sleep(1/fps)  # 60 FPS            
            window.draw()

    @staticmethod
    def handle_inputs() : 
        pass