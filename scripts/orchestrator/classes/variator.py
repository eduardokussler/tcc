from classes.nvidia_smi_wrapper import *

class Variator:
    def __init__(self):
        # All clocks are in MHz
        self.possible_frequencies = {'memory': NvidiaSmi.load_possible_frequecies_to_list('memory'), 
                                     'sm': NvidiaSmi.load_possible_frequecies_to_list('sm')}
        self.current_frequencies = {'memory': self.possible_frequencies['memory'][0], 
                                    'sm': self.possible_frequencies['sm'][0]}
    """ Type is: 'memory' or 'sm'
        Returns true if change was made and false if it was not possible
    """
    def variate_frequency_up(self, type:str):
        step = 2
        current_frequency_index = self.possible_frequencies[type].index(self.current_frequencies[type])
        if current_frequency_index + step >= len(self.possible_frequencies[type]):
            return False 
        self.current_frequencies[type] = self.possible_frequencies[type][current_frequency_index+step]
        NvidiaSmi.set_frequency(self.current_frequencies)
        return True