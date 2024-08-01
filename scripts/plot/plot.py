import seaborn
import sys
from classes.telemetry_model import Telemetry


'''Usage: python3 plot.py <telemetry_file>'''
#print(sys.argv)
data_file = sys.argv[1]

'''File has the following structure:
    #Time        gpu   pwr gtemp mtemp    sm   mem   enc   dec  mclk  pclk
    #HH:MM:SS    Idx     W     C     C     %     %     %     %   MHz   MHz
'''

#key: str(sm frequency) + '_' str(mem frequency). Value: array of readings (class telementry_model.Telemetry)
telemetry_data: dict[str, list] = dict()

with open(data_file, 'r') as data:
    lines = data.readlines()
    for line in lines:
        telemetry:Telemetry = Telemetry.parse_from_file(line)
        if telemetry is not None:
            if telemetry.dict_index not in telemetry_data:
                telemetry_data[telemetry.dict_index] = []
            telemetry_data[telemetry.dict_index].append(telemetry)
    
for key, values in telemetry_data.items():
    print(key)
    for value in values:
        print(values, sep="\n",end="\n \n \n")