from dataclasses import dataclass


@dataclass
class Telemetry:
    timestamp: str
    gpu_idx: int
    power: int  # watts
    gpu_temp: int  # celsius
    mem_temp: int  # celsius
    sm_usage: int  # percentage
    mem_usage: int  # percetage
    encoder_usage: int  # percentage
    decoder_usage: int  # percentage
    mem_clock: int  # Mhz
    sm_clock: int  # Mhz
    dict_index: str

    @staticmethod
    def parse_from_file(line: str) -> str | type["Telemetry"]:
        split_line = line.split(" ")
        split_line = list(filter(lambda val: val != "", split_line))
        if len(split_line) <= 2:  # header saying the sm frequency
            return line
        if "#" in split_line[0]:  # header of nvidia-smi dmon
            return
        split_line = list(map(lambda val: val if val != "-" else 0, split_line))

        timestamp = split_line[0]
        gpu_idx = int(split_line[1])
        power = int(split_line[2])
        gpu_temp = int(split_line[3])
        mem_temp = int(split_line[4])
        sm_usage = int(split_line[5])
        mem_usage = int(split_line[6])
        encoder_usage = int(split_line[7])
        decoder_usage = int(split_line[8])
        mem_clock = int(split_line[9])
        sm_clock = int(split_line[10])
        dict_index = str(sm_clock) + "_" + str(mem_clock)
        telemetry = Telemetry(
            timestamp,
            gpu_idx,
            power,
            gpu_temp,
            mem_temp,
            sm_usage,
            mem_usage,
            encoder_usage,
            decoder_usage,
            mem_clock,
            sm_clock,
            dict_index,
        )
        return telemetry

    def __repr__(self):
        string_return = ""
        string_return += "timestamp: " + str(self.timestamp) + " "
        string_return += "gpu_idx: " + str(self.gpu_idx) + " "
        string_return += "power: " + str(self.power) + " "
        string_return += "gpu_temp: " + str(self.gpu_temp) + " "
        string_return += "mem_temp: " + str(self.mem_temp) + " "
        string_return += "sm_usage: " + str(self.sm_usage) + " "
        string_return += "mem_usage: " + str(self.mem_usage) + " "
        string_return += "encoder_usage: " + str(self.encoder_usage) + " "
        string_return += "decoder_usage: " + str(self.decoder_usage) + " "
        string_return += "mem_clock: " + str(self.mem_clock) + " "
        string_return += "sm_clock: " + str(self.sm_clock) + " "
        string_return += "dict_index: " + str(self.dict_index) + " "
        return string_return + "\n"
