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
from classes.variator import Variator
from classes.utils import *
from classes.nvidia_smi_wrapper import NvidiaSmi
from classes.telemetry import Telemetry



class Orchestrator:
    def __init__(self):
        self.variator = Variator()
    
    def perform_experiment(self, run_script, measurements_interval:float=1):
        NvidiaSmi.reset_frequencies()
        valid_frequency = True
        # Use name of script as output file
        telemetry_thread = Telemetry(run_script.split('/').pop().split('.')[0])
        telemetry_thread.start_telemetry_thread(measurements_interval)


        '''Run experiment for all available sm frequencies'''
        while valid_frequency:
            subprocess.run(run_script, shell=True)
            valid_frequency = self.variator.variate_frequency_up('sm')

        NvidiaSmi.reset_frequencies()
        valid_frequency = True

        '''Run experiment for all available memory frequencies'''
        while valid_frequency:
            subprocess.run(run_script, shell=True)
            valid_frequency = valid_frequency = self.variator.variate_frequency_up('memory')
        

        
        telemetry_thread.running = False

        while not telemetry_thread.stopped:
            time.sleep(1)


