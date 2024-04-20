'''Class to interact with the nvidia-smi commands'''

import subprocess
import os.path
from threading import Thread
from classes.utils import Platform


class NvidiaSmi():

    @staticmethod
    def set_persistence():
        command = 'nvidia-smi -pm 1'
        subprocess.run(command, shell=True)

    '''Load the list of available frequencies for the specified type: sm or memory'''
    @staticmethod
    def load_possible_frequecies_to_list(frequency_type:str) -> list :
        sm_clock_command = 'nvidia-smi --query-supported-clocks=graphics --format csv'
        memory_clock_command = 'nvidia-smi --query-supported-clocks=memory --format csv'
        csv_result = ''
        if frequency_type == 'sm':
            result = subprocess.run(sm_clock_command, capture_output=True, text=True, shell=True)
            csv_result = result.stdout
        else:
            result = subprocess.run(memory_clock_command, capture_output=True, text=True, shell=True)
            csv_result = result.stdout
        
        # Separate text at each new line
        csv_result = csv_result.split('\n')
        # Ignore the csv header
        csv_result = csv_result[1:]
        # only get the number part
        result_set = [row.split(' ')[0] for row in csv_result]
        result_set = set(filter(lambda entry : entry != '', result_set))
        result_set = set(map(lambda entry : int(entry), result_set))
        result_list = list(result_set)
        result_list.sort()
        return result_list
    
    '''Get the default frequency for type
    '''
    @staticmethod
    def get_default_frequency(frequency_type:str, platform:Platform) -> int:
        sm_clock_command = ''
        memory_clock_command = ''
        if platform != Platform.GEFORCE:
            sm_clock_command = 'nvidia-smi --query-gpu=clocks.default_applications.graphics --format csv'
            memory_clock_command = 'nvidia-smi --query-gpu=clocks.default_applications.memory --format csv'
        else:
            NvidiaSmi.reset_frequencies(platform)
            sm_clock_command = 'nvidia-smi --query-gpu=clocks.current.sm --format csv'
            memory_clock_command = 'nvidia-smi --query-gpu=clocks.current.memory --format csv'

        csv_result = ''
        if frequency_type == 'sm':
            result = subprocess.run(sm_clock_command, capture_output=True, text=True, shell=True)
            csv_result = result.stdout
        else:
            result = subprocess.run(memory_clock_command, capture_output=True, text=True, shell=True)
            csv_result = result.stdout
        
        # Separate text at each new line
        csv_result = csv_result.split('\n')
        # Ignore the csv header
        csv_result = csv_result[1:]
        # only get the number part
        result_list = [row.split(' ')[0] for row in csv_result]
        result_list = list(filter(lambda entry : entry != '', result_list))
        result_list = list(map(lambda entry : int(entry), result_list))
        return int(result_list[0])
    
    '''Set the specified frequencies on the gpu'''
    @staticmethod
    def set_frequency(frequency_mhz:dict, platform:Platform):
        command = {Platform.ENTERPRISE: f'nvidia-smi --applications-clocks={frequency_mhz["memory"]},{frequency_mhz["sm"]}',
                   Platform.GEFORCE: f'nvidia-smi --lock-gpu-clocks {frequency_mhz["sm"]},{frequency_mhz["sm"]}',
                   Platform.GPPD: f'gpu_control {frequency_mhz["memory"]} {frequency_mhz["sm"]}'
                   }
        subprocess.run(command[platform], shell=True)

    @staticmethod
    def reset_frequencies(platform:Platform):
        command = {Platform.ENTERPRISE: 'nvidia-smi --reset-applications-clocks',
                   Platform.GPPD: 'nvidia-smi --reset-applications-clocks',
                   Platform.GEFORCE: 'nvidia-smi --reset-gpu-clocks'}
        subprocess.run(command[platform], shell=True, capture_output=True, text=True)

    
    '''Get gpu performance data
        power(watts)
        temperature(celsius)
        memory usage (%)
        sm usage (%)
        
        returns the output as string

    '''
    @staticmethod
    def get_telemetry_data() -> str:
        command = f'nvidia-smi dmon --count 1 -o T'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout

    