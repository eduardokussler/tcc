'''This script's purpose is to manage 3 main areas:
    Running the project
    Vary the frequencies of operation of memory and sm clock
    Collect the data from nvidia-smi
        - Power
        - Temperature
        - Memory usage
        - Sm usage
'''
import subprocess
import time
import logging
from classes.variator import Variator
from classes.utils import *
from classes.nvidia_smi_wrapper import NvidiaSmi
from classes.telemetry import Telemetry
from classes.utils import Platform



class Orchestrator:
    def __init__(self, platform:Platform, run_script:str):
        NvidiaSmi.reset_frequencies(platform)
        self.variator = Variator(platform)
        self.platform = platform
        self.output_file = open('output_results_'+run_script.split('/').pop().split('.')[0], 'w+')
        self.run_script = run_script
        self.log = logging.Logger('Orchestrator')
    
    def perform_experiment(self, measurements_interval:float=1):
        valid_frequency = True
        # Use name of script as output file
        telemetry_thread = Telemetry('telemetry_'+self.run_script.split('/').pop().split('.')[0])
        telemetry_thread.write_new_current_frequencies(self.variator.current_frequencies, self.platform)
        telemetry_thread.start_telemetry_thread(measurements_interval)


        '''Run experiment for all available sm frequencies'''
        while valid_frequency:
            process_output = subprocess.run(f'time {self.run_script}; echo "finished"', shell=True, capture_output=True, text=True).stdout
            self.output_file.write(process_output)
            valid_frequency = self.variator.variate_frequency_up('sm')
            telemetry_thread.write_new_current_frequencies(self.variator.current_frequencies, self.platform)

        if self.platform == Platform.ENTERPRISE:
            NvidiaSmi.reset_frequencies()
            valid_frequency = True

            '''Run experiment for all available memory frequencies'''
            while valid_frequency:
                process_output = subprocess.run(f'time {self.run_script}', shell=True, capture_output=True, text=True).stdout
                self.output_file.write(process_output)
                valid_frequency = valid_frequency = self.variator.variate_frequency_up('memory')
                telemetry_thread.write_new_current_frequencies(self.variator.current_frequencies, self.platform)


        telemetry_thread.running = False
        self.output_file.flush()
        self.output_file.close()
        telemetry_thread.thread.join()


