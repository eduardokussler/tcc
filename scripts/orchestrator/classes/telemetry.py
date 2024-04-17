
from threading import Thread
from classes.nvidia_smi_wrapper import NvidiaSmi
import time


class Telemetry:
    def __init__(self, filename):
        self.running = True
        self.thread = None
        self.output = open(filename, 'wt')
        self.stopped = False
        self.string_result = ''

    '''Creates a thread object running the get telemetry function
        Returns the thread for joining purposes
    '''
    def start_telemetry_thread(self, interval:float=1):
        self.thread = Thread(target=self.get_telemetry_data, args=(self, interval))
        self.thread.start()
    
    '''Runs a loop and gets the output of dmon from nvidia-smi
        Use float inputs to get ms precision'''
    def get_telemetry_data(self, interval:float=1):
        first_loop = True
        
        while self.running:
            command_output = NvidiaSmi.get_telemetry_data()
            command_output = command_output.splitlines()
            if (first_loop):
                self.string_result += command_output[0]
                self.string_result += command_output[1]
                first_loop = False
            command_output += command_output[2]

            time.sleep(interval)
        self.output.write(self.string_result)
        self.output.flush()
        self.output.close()
        self.stopped = True
    
