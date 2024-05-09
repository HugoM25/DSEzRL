import time
import multiprocessing
from desmume.emulator import DeSmuME
import random 

from .DSCommand import DSCommand
from .DSInstance import DSInstance

class DSManager: 
    def __init__(self, rom_path: str, nb_instances:int = 1) -> None:
        self.rom_path = rom_path 
        self.nb_instances = nb_instances
        self.processes = []

        # Create queue for communication with the processes and the master
        self.process_requests = [multiprocessing.Queue() for _ in range(self.nb_instances)]

        # Create queue for communicqtion with the processes and the master
        self.process_responses = [multiprocessing.Queue() for _ in range(self.nb_instances)]

        
        for process_index in range(self.nb_instances):
            process = multiprocessing.Process(
                target=DSInstance.run_emulator,
                args=(self.rom_path, True, 60, self.process_requests[process_index], self.process_responses[process_index])
            )
            self.processes.append(process)
            process.start()

    def send_command(self, command: DSCommand) -> None:
  
        time_taken = time.time()

        command_id = command.generate_command_id()
        # Send command to the process
        self.process_requests[command.target_instance_index].put((command_id, command))

        # Wait for the response
        timeout_response = time.time() + 5
        while time.time() < timeout_response :
            if not self.process_responses[command.target_instance_index].empty():
                response_id, response = self.process_responses[command.target_instance_index].get()
                if response_id == command_id:
                    print(f'Response received in {time.time() - time_taken}s')
                    return response

        return None
