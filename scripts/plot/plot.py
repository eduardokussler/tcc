import seaborn
import sys
import pandas
import dataclasses
from classes.telemetry_model import Telemetry
from datetime import datetime, timedelta

# specifyu the time format used on the measurements
FMT = '%H:%M:%S'


'''Usage: python3 plot.py <telemetry_file>'''
#print(sys.argv)
data_file = sys.argv[1]

'''File has the following structure:
    #Time        gpu   pwr gtemp mtemp    sm   mem   enc   dec  mclk  pclk
    #HH:MM:SS    Idx     W     C     C     %     %     %     %   MHz   MHz
'''

#key: str(sm frequency) + '_' str(mem frequency). Value: array of readings (class telementry_model.Telemetry)
telemetry_data: dict[str, list] = dict()
# Telemetry class instances list read from file in sequence
telemetry_list: list[Telemetry] = []

with open(data_file, 'r') as data:
    lines = data.readlines()
    for line in lines:
        # Parse from file can return empty line for unused frequency on the first reading
        telemetry:Telemetry = Telemetry.parse_from_file(line)
        if telemetry is not None:
            if telemetry.dict_index not in telemetry_data:
                telemetry_data[telemetry.dict_index] = []
            telemetry_data[telemetry.dict_index].append(telemetry)
            telemetry_list.append(telemetry)

# cleaning unwanted value for unused frequency or when application already stopped using the gpu[
for key, tel_list in telemetry_data.items():
    telemetry_data[key] = list(filter(lambda tel: tel.sm_usage > 0, tel_list))
# for key, values in telemetry_data.items():
#     print(key)
#     for value in values:
#         print(values, sep="\n",end="\n \n \n")



plot_data = pandas.DataFrame(telemetry_list, columns=[field.name for field in dataclasses.fields(Telemetry)])
axes = seaborn.lineplot(plot_data, x="sm_clock", y="power")
figure = axes.get_figure()
figure.savefig("sm_clock_to_power.png") 

# process time spent on each clock configuration
# calculate the total power spent to finish processing

# key: str(sm frequency) + '_' str(mem frequency) -> (start_time, end_time)
time_of_start_and_end: dict[str, tuple] = dict()
#key: str(sm frequency) + '_' str(mem frequency) -> total power
total_power_data: dict[str, int] = dict()
#key: str(sm frequency) + '_' str(mem frequency) -> number of observations
total_obeservations: dict[str, int] = dict()

for key, telemetry_listing in telemetry_data.items():
    for telemetry in telemetry_listing:
        if key not in total_power_data:
            total_power_data[key] = 0
            total_obeservations[key] = 0
        total_power_data[key] += telemetry.power
        total_obeservations[key] += 1
        timestamp = datetime.strptime(telemetry.timestamp, FMT)
        if key not in time_of_start_and_end:
            time_of_start_and_end[key] = (timestamp, timestamp)
        else:
            current_data = time_of_start_and_end[key]
            time_of_start_and_end[key] = (min(timestamp, current_data[0]), max(timestamp, current_data[1]))
print(f'Start and endTime {time_of_start_and_end}')
# Because the collecting of each data point was not the same across all applications, 
# Take the average from the power measured over the number of observations
# Multiply by the total time took (in seconds)
for key in total_power_data.keys():
    total_time_took:timedelta = time_of_start_and_end[key][1] - time_of_start_and_end[key][0]
    print(f'Seconds took {total_time_took.total_seconds()}')
    total_power_data[key] = (total_power_data[key]/total_obeservations[key]) * total_time_took.total_seconds()

print(total_power_data)
total_power_data = pandas.DataFrame(total_power_data.values(), index=[key for key in total_power_data.keys()])
# not looking good at the moment
axes = seaborn.lineplot(total_power_data, x=total_power_data.index, y=0)
figure = axes.get_figure()
figure.savefig("total_power_per_config.png") 

