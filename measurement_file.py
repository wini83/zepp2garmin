import csv
from datetime import datetime, timedelta
from typing import List

from measurement import Measurement


def generate_list(list_mes: List[Measurement]):
    result = []
    for item in list_mes:
        row = item.to_list()
        row.insert(0, len(result) + 1)
        result.append(row)
    return result





class MeasurementsFile:
    measurements: List[Measurement]
    filtered_list: List[Measurement]
    groups: int

    def __init__(self):
        self.measurements = []

    def load_from_csv(self, file_name):
        csv_reader = csv.reader(file_name, delimiter=',')
        for row in csv_reader:
            if csv_reader.line_num > 1:
                if len(row) == 10:
                    item = Measurement(row)
                    self.measurements.append(item)
        self.filtered_list = self.measurements

    def filter_by_date(self, date_start: datetime, date_end: datetime):
        date_end2 = date_end + timedelta(days=1)
        date_end2 = date_end2.replace(hour=0, minute=0)
        self.filtered_list = list(filter(lambda x: date_end2 > x.timestamp > date_start, self.filtered_list))

    def filter_by_height(self, height):
        if height != -1:
            self.filtered_list = list(filter(lambda x: x.height == height, self.filtered_list))

    def group_by_date(self, tolerance_secs=300):
        group_id = 0
        for i in range(2, len(self.filtered_list)):
            time_diff = self.filtered_list[i].timestamp - self.filtered_list[i - 1].timestamp
            if time_diff.total_seconds() < tolerance_secs:
                if self.filtered_list[i - 1].group is None:
                    group_id = group_id + 1
                    self.filtered_list[i - 1].group = group_id
                    self.filtered_list[i - 1].chosen = True
                self.filtered_list[i].group = group_id
        self.groups = group_id

    def choose_from_group(self, index: int):
        self.filtered_list[index].chosen = True
        item_id = 0
        group = self.filtered_list[index].group
        for item in self.filtered_list:
            if item.group == group:
                if index != item_id:
                    item.chosen = None
                else:
                    item.chosen = True
            item_id += 1

    def filter_chosen(self):
        self.filtered_list = list(
            filter(lambda x: (x.group is not None and x.chosen) or (x.group is None), self.filtered_list))
        for item in self.filtered_list:
            item.group = None
            item.chosen = None
