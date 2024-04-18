
from threading import Thread, Lock
from classes.nvidia_smi_wrapper import NvidiaSmi
import time


class Telemetry:
    def __init__(self, filename):
        self.running = True
        self.thread = None
        self.output_file = open(filename, 'w+')
        self.stopped = False
        self.string_result = ''
        self.lock = Lock()
        self.print_header = True

    '''Creates a thread object running the get telemetry function
        Returns the thread for joining purposes
    '''
    def start_telemetry_thread(self, interval:float=1):
        self.thread = Thread(target=self.get_telemetry_data, args=(interval,), daemon=True)
        self.thread.start()
    
    '''Runs a loop and gets the output of dmon from nvidia-smi
        Use float inputs to get ms precision'''
    def get_telemetry_data(self, interval:float=1):
        self.print_header = True
        loops = 0
        while self.running:
            self.lock.acquire()
            command_output = NvidiaSmi.get_telemetry_data()
            command_output = command_output.splitlines()
            if (self.print_header):
                self.string_result += command_output[0] + '\n'
                self.string_result += command_output[1] + '\n'
                self.print_header = False

            self.string_result += command_output[2] + '\n'
            loops+=1
            if (loops >= 100):
                self.output_file.write(self.string_result)
                loops=0
                self.string_result=''
            self.lock.release()
            time.sleep(interval)

        self.output_file.write(self.string_result)
        self.output_file.flush()
        self.output_file.close()
        self.stopped = True
    
    def write_new_current_frequencies(self, frequencies: dict):
        self.lock.acquire()
        self.string_result = self.string_result + '\n' + f'Memory: {frequencies["memory"]}MHz  SMs: {frequencies["sm"]}MHz\n'
        self.print_header = True
        self.lock.release()
