from datetime import datetime
from typing import List, Optional


def parse_float(string: str) -> Optional[float]:
    if string == "null":
        return None
    try:
        return float(string)
    except ValueError:
        return None


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
    height: int
    bmi: float
    fatRate: float
    bodyWaterRate: float
    boneMass: float
    metabolism: int
    muscleRate: float
    visceralFat: int
    timestamp: datetime

    def __init__(self, csv_line: List[str] = None):
        self.timestamp_str = csv_line[0]
        self.weight = parse_float(csv_line[1])
        self.height = parse_int(csv_line[2])
        self.bmi = parse_float(csv_line[3])
        self.fatRate = parse_float(csv_line[4])
        self.bodyWaterRate = parse_float(csv_line[5])
        self.boneMass = parse_float(csv_line[6])
        self.metabolism = parse_int(csv_line[7])
        self.muscleRate = parse_float(csv_line[8])
        self.visceralFat = parse_int(csv_line[9])
        self.timestamp = parse_date(self.timestamp_str)
