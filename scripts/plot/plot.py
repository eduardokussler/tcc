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
"""Usage: python3 plot.py <machine origin of the data> <fraction of samples to consider -> 1/this_parameter> <telemetry_file1 telemetry_file2 telemetry_file3...>"""
# print(sys.argv)
machine_name = sys.argv[1]
fraction_of_samples_to_consider = int(sys.argv[2])
data_files = sys.argv[3:]

"""File has the following structure:
    #Time        gpu   pwr gtemp mtemp    sm   mem   enc   dec  mclk  pclk
    #HH:MM:SS    Idx     W     C     C     %     %     %     %   MHz   MHz
"""

# key: str(sm frequency) + '_' str(mem frequency). Value: array of readings (class telementry_model.Telemetry)
telemetry_data: dict[str, list] = dict()
# Telemetry class instances list read from file in sequence
telemetry_list: list[Telemetry] = []

# tuple of proxy app name and data
total_power_data_per_proxy_app: list[tuple] = list()
plt.figure(figsize=(8.5, 6.38))

for data_file_path in data_files:
    with open(data_file_path, "r") as data:
        lines = data.readlines()
        current_sm_clock = ""
        skip = False
        available_sm_clocks = set()
        for line in lines:
            # Parse from file can return empty line for unused frequency on the first reading
            telemetry = Telemetry.parse_from_file(line)
            if type(telemetry) is str:
                current_sm_clock = telemetry
                available_sm_clocks.add(current_sm_clock)
            if len(available_sm_clocks) % fraction_of_samples_to_consider == 0:
                skip = False
            else:
                skip = True
            if telemetry is not None and type(telemetry) is not str and not skip:
                # Ignore telemetry that doesn't match the specified clock
                if str(telemetry.sm_clock) not in current_sm_clock:
                    continue
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
    # mask = plot_data["sm_clock"] == 2550
    # print(plot_data.loc[mask])
    axes = seaborn.lineplot(
        plot_data,
        x="sm_clock",
        y="power",
        errorbar=None,
        markers=False,
        dashes=False,
        # style="sm_clock",
    )  # [".", "x", "+", "o"])
    # axes.set_title("Power needed to operate at each configuration")
    axes.set_title(
        f"Potência necessária para a GPU operar em cada frequência - {data_file_name}/{machine_name}"
    )
    axes.ticklabel_format(style="plain")
    axes.set(xlabel="Sm clock (MHz)", ylabel="Potência (Watts)")
    figure = axes.get_figure()
    figure.savefig(f"sm_clock_to_power_{data_file_name}_{machine_name}.png")
    plt.clf()
    # process time spent on each clock configuration
    # calculate the total power spent to finish processing

    # key: str(sm frequency) + '_' str(mem frequency) -> (start_time, end_time)
    time_of_start_and_end: dict[str, tuple] = dict()
    total_power_data: pandas.DataFrame = pandas.DataFrame(
        columns=["sm_clock", "total power", "total time", "name"], data=None
    )
    # key: str(sm frequency) + '_' str(mem frequency) -> number of observations
    total_obeservations: dict[str, int] = dict()

    for _, telemetry_listing in telemetry_data.items():
        for telemetry in telemetry_listing:
            key = str(
                telemetry.sm_clock
            )  # Change _ to key if memory frequency is desired
            mask = total_power_data["sm_clock"] == key
            if len(total_power_data[mask]) == 0:
                total_power_data.loc[len(total_power_data)] = [
                    key,
                    0.0,
                    None,
                    data_file_name,
                ]
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
        ) * max(total_time_took.total_seconds(), 1)
        total_power_data.loc[mask, "total time"] = max(
            total_time_took.total_seconds(), 1
        )
        print(f"Total power consumed: {total_power_data.loc[mask, 'total power']}")

    total_power_data_per_proxy_app.append((data_file_name, total_power_data))
    print(total_power_data)
    axes = seaborn.barplot(total_power_data, x="sm_clock", y="total power")
    # axes.set_title("Total power (Watts) consumed for each clock configuration")
    axes.set_title(
        f"Potência total consumida para rodar o {data_file_name} em cada configuração - {machine_name}"
    )
    axes.set(xlabel="Sm clock (MHz)", ylabel="Potência total(Watts)")
    axes.ticklabel_format(style="plain", axis="y")
    axes.tick_params(axis="x", labelrotation=45)
    axes.xaxis.tick_bottom()
    figure = axes.get_figure()
    figure.savefig(f"total_power_per_config_{data_file_name}_{machine_name}.png")
    plt.clf()

    # graph the total time () took for each config
    axes = seaborn.barplot(total_power_data, x="sm_clock", y="total time")
    # axes.set_title("Total time () taken each clock configuration")
    axes.set_title(f"Tempo total para rodar - {data_file_name}/{machine_name}")
    axes.ticklabel_format(style="plain", axis="y")
    axes.set(xlabel="Sm clock (MHz)", ylabel="Tempo total (Segundos)")
    axes.tick_params(axis="x", labelrotation=45)
    axes.xaxis.tick_bottom()
    figure = axes.get_figure()
    figure.savefig(f"total_time_per_config_{data_file_name}_{machine_name}.png")
    plt.clf()

    mem_and_sm_usage: pandas.DataFrame = pandas.DataFrame(
        columns=["sm_clock", "usage", "type"], data=None
    )
    for usage_type in ["sm_usage", "mem_usage"]:
        for _, telemetry_listing in telemetry_data.items():
            for telemetry in telemetry_list:
                mem_and_sm_usage.loc[len(mem_and_sm_usage)] = [
                    telemetry.sm_clock,
                    telemetry.mem_usage
                    if usage_type == "mem_usage"
                    else telemetry.sm_usage,
                    "Mem" if usage_type == "mem_usage" else "SM",
                ]
    print(mem_and_sm_usage)
    # Plot memory usage and SM usage to see if it hit a bottleneck
    axes = seaborn.barplot(
        mem_and_sm_usage, x="sm_clock", y="usage", hue="type", errorbar=None
    )
    axes.set_title(f"Uso de SM e Memória - {data_file_name}/{machine_name}")
    axes.ticklabel_format(style="plain", axis="y")
    # axes.set(xlabel="Sm clock (MHz)", ylabel="Tempo total (Segundos)")
    axes.tick_params(axis="x", labelrotation=45)
    # axes.xaxis.tick_bottom()
    plt.title(f"Uso de SM e Memória - {data_file_name}/{machine_name}")
    plt.xticks(rotation=45)
    plt.ylabel("Uso (%)")
    figure = axes.get_figure()
    figure.savefig(f"memory_and_sm_usage_{data_file_name}_{machine_name}.png")
    plt.clf()


names = list(map(lambda x: x[0], total_power_data_per_proxy_app))
# for total_power_data_tuple in total_power_data_per_proxy_app:
#     total_power_data_df = total_power_data_tuple[1]
total_power_data_df = pandas.DataFrame()
for total_power_data_tuple in total_power_data_per_proxy_app:
    total_power_data_df = pandas.concat(
        [total_power_data_df, total_power_data_tuple[1]]
    )
# graph all times of all apps on the same figure
axes = seaborn.lineplot(
    total_power_data_df,
    x="sm_clock",
    y="total power",
    legend=True,
    errorbar=None,
    hue="name",
    dashes=False,
    # style="sm_clock",  markers=False
)
# axes.set_title("Total time () taken each clock configuration")
axes.set_title(f"Tempo total para rodar todos os proxy apps - {machine_name}")
axes.ticklabel_format(style="plain", axis="y")
axes.set(xlabel="Sm clock (MHz)", ylabel="Potência total (Watts)")
axes.tick_params(axis="x", labelrotation=45)
axes.xaxis.tick_bottom()
plt.legend(title="Proxy app")
figure = axes.get_figure()
figure.savefig(f"total_power_per_config_all_apps_{machine_name}.png")
