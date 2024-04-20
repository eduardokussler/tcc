import logging
from classes.nvidia_smi_wrapper import *
from classes.utils import Platform

class Variator:
    def __init__(self, platform:Platform):
        self.platform = platform
        # All clocks are in MHz
        self.possible_frequencies = {'memory': NvidiaSmi.load_possible_frequecies_to_list('memory'), 
                                     'sm': NvidiaSmi.load_possible_frequecies_to_list('sm')}
        self.current_frequencies = {'memory': self.possible_frequencies['memory'][0], 
                                    'sm': self.possible_frequencies['sm'][0]}
        self.default_frequencies = {'memory': NvidiaSmi.get_default_frequency('memory', platform), 
                                    'sm': NvidiaSmi.get_default_frequency('sm', platform)}
        self.logger =  logging.getLogger(__name__)
        NvidiaSmi.set_frequency(self.current_frequencies, self.platform)
    """ Type is: 'memory' or 'sm'
        Returns true if change was made and false if it was not possible
    """
    def variate_frequency_up(self, type:str):
        step = 2
        current_frequency_index = self.possible_frequencies[type].index(self.current_frequencies[type])
        if current_frequency_index + step >= len(self.possible_frequencies[type]):
            return False 
        self.current_frequencies[type] = self.possible_frequencies[type][current_frequency_index+step]
        frequencies = {'memory': self.current_frequencies['memory'] if type == 'memory' else self.default_frequencies['memory'], 
                       'sm': self.current_frequencies['sm'] if type == 'sm' else self.default_frequencies['sm']}
        self.logger.info(f'Setting frequencies to: memory={frequencies["memory"]} and sm={frequencies["sm"]}')
        NvidiaSmi.set_frequency(frequencies, self.platform)
        return True