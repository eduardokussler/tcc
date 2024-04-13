'''Class to interact with the nvidia-smi commands'''

import subprocess


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
        result_list = [row.split(' ')[0] for row in csv_result]
        result_list = list(filter(lambda entry : entry != '', result_list))
        result_list = list(map(lambda entry : int(entry), result_list))
        result_list.sort()
        return result_list
    
    '''Set the specified frequencies on the gpu'''
    @staticmethod
    def set_frequency(frequency_mhz:dict):
        command = f'nvidia-smi -ac={frequency_mhz["memory"]},{frequency_mhz["sm"]}'
        subprocess.run(command, shell=True)

    @staticmethod
    def reset_frequencies():
        command = 'nvidia-smi --reset-applications-clocks'
        subprocess.run(command, shell=True)
