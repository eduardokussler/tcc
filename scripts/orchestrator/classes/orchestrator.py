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
from classes.variator import *
from classes.utils import *
from classes.nvidia_smi_wrapper import *



class Orchestrator:
    def __init__(self):
        self.variator = Variator()
    
    def perform_experiment(self, run_script):
        NvidiaSmi.reset_frequencies()
        valid_frequency = True
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


