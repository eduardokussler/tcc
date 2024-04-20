from enum import Enum

class Platform(Enum):
    GEFORCE = 1
    ENTERPRISE = 2
    GPPD = 3

    @staticmethod
    def from_str(label:str):
        label = label.upper()
        if label == 'GEFORCE':
            return Platform.GEFORCE
        elif label == 'ENTERPRISE':
            return Platform.ENTERPRISE
        elif label == 'GPPD':
            return Platform.GPPD
        else:
            raise NotImplementedError