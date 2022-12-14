from datetime import datetime
from typing import List, Optional


def parse_float(string: str) -> Optional[float]:
    if string == "null":
        return None
    try:
        return float(string)
    except ValueError:
        return None


def format_float(float_inp):
    if float_inp is None:
        output_str = "N/A"
    else:
        output_str = f'{float_inp:.2f}'
    return output_str


def parse_int(string: str) -> Optional[int]:
    if string == "null":
        return None
    try:
        return int(string)
    except ValueError:
        return None


def parse_date(string_input: str) -> datetime:
    shorted = string_input[0:19]
    format_str = "%Y-%m-%d %H:%M:%S"
    result = datetime.strptime(shorted, format_str)
    return result


class Measurement:
    timestamp_str: str
    weight: float = None
    height: float
    bmi: float
    fatRate: float
    bodyWaterRate: float
    boneMass: float
    metabolism: float
    muscleRate: float
    visceralFat: float
    timestamp: datetime
    group: int = None
    chosen: bool = None

    def __init__(self, csv_line: List[str] = None):
        if csv_line is not None:
            self.timestamp_str = csv_line[0]
            self.weight = parse_float(csv_line[1])
            self.height = parse_float(csv_line[2])
            self.bmi = parse_float(csv_line[3])
            self.fatRate = parse_float(csv_line[4])
            self.bodyWaterRate = parse_float(csv_line[5])
            self.boneMass = parse_float(csv_line[6])
            self.metabolism = parse_float(csv_line[7])
            self.muscleRate = parse_float(csv_line[8])
            self.visceralFat = parse_float(csv_line[9])
            self.timestamp = parse_date(self.timestamp_str)

    @property
    def status(self):
        if self.group is None:
            return None
        else:
            result = str(self.group)
            if self.chosen:
                result += "*"
            return result

    @property
    def weight_formatted(self) -> str:
        return format_float(self.weight)

    @property
    def muscle_rate_formatted(self) -> str:
        return format_float(self.muscleRate)



    def to_list(self):
        return [self.timestamp,
                format_float(self.weight),
                format_float(self.height),
                format_float(self.bmi),
                format_float(self.fatRate),
                format_float(self.bodyWaterRate),
                format_float(self.boneMass),
                format_float(self.metabolism),
                format_float(self.muscleRate),
                format_float(self.visceralFat),
                self.status]
