import seaborn
import sys
import pandas
import dataclasses
import matplotlib.pyplot as plt
from classes.telemetry_model import Telemetry
from datetime import datetime, timedelta

# specifyu the time format used on the measurements
FMT = "%H:%M:%S"

# Don't use scientific notation on pandas.
pandas.options.display.float_format = "{:,.3f}".format

seaborn.set_theme()
"""Usage: python3 plot.py <telemetry_file1 telemetry_file2 telemetry_file3...>"""
# print(sys.argv)
data_files = sys.argv[1:]

"""File has the following structure:
    #Time        gpu   pwr gtemp mtemp    sm   mem   enc   dec  mclk  pclk
    #HH:MM:SS    Idx     W     C     C     %     %     %     %   MHz   MHz
"""

# key: str(sm frequency) + '_' str(mem frequency). Value: array of readings (class telementry_model.Telemetry)
telemetry_data: dict[str, list] = dict()
# Telemetry class instances list read from file in sequence
telemetry_list: list[Telemetry] = []
for data_file_path in data_files:
    with open(data_file_path, "r") as data:
        lines = data.readlines()
        for line in lines:
            # Parse from file can return empty line for unused frequency on the first reading
            telemetry: Telemetry = Telemetry.parse_from_file(line)
            if telemetry is not None:
                if telemetry.dict_index not in telemetry_data:
                    telemetry_data[telemetry.dict_index] = []
                telemetry_data[telemetry.dict_index].append(telemetry)
                telemetry_list.append(telemetry)
    index_of_last_underscore = data_file_path.rfind("_")
    data_file_name = data_file_path[index_of_last_underscore + 1 :]
    # cleaning unwanted value for unused frequency or when application already stopped using the gpu
    telemetry_list = list(filter(lambda tel: tel.sm_usage > 0, telemetry_list))
    for key, tel_list in telemetry_data.items():
        telemetry_data[key] = list(filter(lambda tel: tel.sm_usage > 0, tel_list))
    # for key, values in telemetry_data.items():
    #     print(key)
    #     for value in values:
    #         print(values, sep="\n",end="\n \n \n")

    plot_data = pandas.DataFrame(
        telemetry_list, columns=[field.name for field in dataclasses.fields(Telemetry)]
    )
    print(plot_data)
    axes = seaborn.lineplot(plot_data, x="sm_clock", y="power", errorbar=None)
    axes.set_title("Power needed to operate at each configuration")
    figure = axes.get_figure()
    figure.savefig(f"sm_clock_to_power_{data_file_name}.png")
    plt.clf()
    # process time spent on each clock configuration
    # calculate the total power spent to finish processing

    # key: str(sm frequency) + '_' str(mem frequency) -> (start_time, end_time)
    time_of_start_and_end: dict[str, tuple] = dict()
    total_power_data: pandas.DataFrame = pandas.DataFrame(
        columns=["sm_clock", "total power", "total time"], data=None
    )
    # key: str(sm frequency) + '_' str(mem frequency) -> number of observations
    total_obeservations: dict[str, int] = dict()

    for key, telemetry_listing in telemetry_data.items():
        for telemetry in telemetry_listing:
            mask = total_power_data["sm_clock"] == key
            if len(total_power_data[mask]) == 0:
                total_power_data.loc[len(total_power_data)] = [key, 0.0, None]
            if key not in total_obeservations:
                total_obeservations[key] = 0
            # recalculate mask for altered dataframe
            mask = total_power_data["sm_clock"] == key
            total_power_data.loc[mask, "total power"] += telemetry.power
            total_obeservations[key] += 1
            timestamp = datetime.strptime(telemetry.timestamp, FMT)
            if key not in time_of_start_and_end:
                time_of_start_and_end[key] = (timestamp, timestamp)
            else:
                current_data = time_of_start_and_end[key]
                time_of_start_and_end[key] = (
                    min(timestamp, current_data[0]),
                    max(timestamp, current_data[1]),
                )
    print(f"Start and endTime {time_of_start_and_end}")
    # Because the collecting of each data point was not the same across all applications,
    # Take the average from the power measured over the number of observations
    # Multiply by the total time took (in seconds)
    for key in total_power_data.loc[:, "sm_clock"]:
        mask = total_power_data["sm_clock"] == key
        total_time_took: timedelta = (
            time_of_start_and_end[key][1] - time_of_start_and_end[key][0]
        )
        print(f"Seconds took {total_time_took.total_seconds()}")
        total_power_data.loc[mask, "total power"] = (
            total_power_data.loc[mask, "total power"] / total_obeservations[key]
        ) * total_time_took.total_seconds()
        total_power_data.loc[mask, "total time"] = total_time_took.total_seconds()
        print(f"Total power consumed: {total_power_data.loc[mask, 'total power']}")

    print(total_power_data)
    plt.figure(figsize=(16, 8))
    axes = seaborn.barplot(total_power_data, x="sm_clock", y="total power")
    axes.set_title("Total power consumed for each clock configuration")
    axes.tick_params(axis="x", labelrotation=45)
    axes.xaxis.tick_bottom()
    figure = axes.get_figure()
    figure.savefig(f"total_power_per_config_{data_file_name}.png")
    plt.clf()

    # graph the total time took for each config
    axes = seaborn.barplot(total_power_data, x="sm_clock", y="total time")
    axes.set_title("Total time taken each clock configuration")
    axes.tick_params(axis="x", labelrotation=45)
    axes.xaxis.tick_bottom()
    figure = axes.get_figure()
    figure.savefig(f"total_time_per_config_{data_file_name}.png")
    plt.clf()


# graph all times of all apps on the same figure
#
