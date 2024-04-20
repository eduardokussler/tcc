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
        self.variator = Variator(platform)
        self.variator.reset_to_default_frequencies()
        self.platform = platform
        self.output_file = open('output_results_'+run_script.split('/').pop().split('.')[0], 'w+')
        self.run_script = run_script
        self.logger =  logging.getLogger(__name__)
    
    def perform_experiment(self, measurements_interval:float=1):
        valid_frequency = True
        self.variator.set_lowest_frequency('sm')
        # Use name of script as output file
        telemetry_thread = Telemetry('telemetry_'+self.run_script.split('/').pop().split('.')[0])
        telemetry_thread.write_new_current_frequencies(self.variator.current_frequencies, self.platform)
        telemetry_thread.start_telemetry_thread(measurements_interval)


        '''Run experiment for all available sm frequencies'''
        while valid_frequency:
            process = subprocess.run(f'time -f "user %U \nsystem %S \nelapsed %E" {self.run_script};', shell=True, capture_output=True, text=True)
            process_output = process.stdout + '\n \n \n' + process.stderr
            self.output_file.write(process_output)
            valid_frequency = self.variator.variate_frequency_up('sm')
            telemetry_thread.write_new_current_frequencies(self.variator.current_frequencies, self.platform)
        
        
        '''Run experiment for all available memory frequencies'''
        if self.platform != Platform.GEFORCE:
            self.variator.reset_to_default_frequencies()
            self.variator.set_lowest_frequency('memory')
            valid_frequency = True
            while valid_frequency:
                process = subprocess.run(f'time -f "user %U \nsystem %S \nelapsed %E" {self.run_script}', shell=True, capture_output=True, text=True)
                process_output = process.stdout + '\n' + process.stderr
                self.output_file.write(process_output)
                valid_frequency = valid_frequency = self.variator.variate_frequency_up('memory')
                telemetry_thread.write_new_current_frequencies(self.variator.current_frequencies, self.platform)


        telemetry_thread.running = False
        self.output_file.flush()
        self.output_file.close()
        telemetry_thread.thread.join()


