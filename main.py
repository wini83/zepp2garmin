import csv
from datetime import date, timedelta
from os import chdir, path
from typing import List

import click
from loguru import logger
from tabulate import tabulate

from measurement import Measurement

chdir(path.dirname(path.abspath(__file__)))

logger.add("zepp2garmin.log", rotation="1 week")


@click.command()
@click.argument('file_name', type=click.File('r'))
@click.option('--date-start', type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()))
@click.option('--date-end', type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()))
@click.option('--height', type=int, default=-1)
@click.option("--only_read", is_flag=True, help="Run without notifications", default=False)
def main(file_name, date_start, date_end, height, only_read):
    click.echo("")
    click.echo(click.style('zepp2garmin - transfer body composition from Zepp to Garmin Connect',
                           fg='black',
                           bold=True,
                           bg="yellow",
                           blink=True))
    click.echo(f'{"=" * 120}')
    if only_read:
        click.echo("RUNDRY!!!")
    click.echo(f"Start: {date_start}, End: {date_end} ")
    measurements: List[Measurement] = []
    csv_reader = csv.reader(file_name, delimiter=',')
    for row in csv_reader:
        if csv_reader.line_num > 1:
            if len(row) == 10:
                item = Measurement(row)
                measurements.append(item)

    click.echo(f"Measurements in file:  {len(measurements)} (total)")

    date_end2 = date_end + timedelta(days=1)
    date_end2 = date_end2.replace(hour=0, minute=0)

    click.echo(date_end2)

    filtered_list = list(filter(lambda x: date_end2 > x.timestamp > date_start, measurements))

    if height != -1:
        filtered_list = list(filter(lambda x: x.height == height, filtered_list))

    click.echo(f"Measurements filtered:  {len(filtered_list)} ")
    group_id = 0
    for i in range(2, len(filtered_list)):
        time_diff = filtered_list[i].timestamp - filtered_list[i - 1].timestamp
        if time_diff.total_seconds() < 300:
            if filtered_list[i - 1].group is None:
                group_id = group_id + 1
                filtered_list[i-1].group = group_id
                filtered_list[i - 1].chosen = True
            filtered_list[i].group = group_id

    click.echo(generate_table(filtered_list))

    while not click.confirm('Data correct?'):
        for i in range(0, group_id):
            value = click.prompt(f'Enter the ID of the measurement from the Group {i+1} you want to keep', type=int)
            # TODO: check data
            filtered_list[value].chosen = True
            id = 1
            for item in filtered_list:
                if item.group == i+1:
                    if value != id:
                        item.chosen = None
                    else:
                        item.chosen = True
                id += 1
        click.echo(generate_table(filtered_list))

    filtered_list = list(filter(lambda x: (x.group is not None and x.chosen) or (x.group is None), filtered_list))
    click.echo(generate_table(filtered_list))





def generate_table(list_mes: List[Measurement]):
    result = []
    headers_list = ["ID", 'time', 'weight', 'height', 'bmi', 'fatRate', 'bodyWaterRate', 'boneMass', 'metabolism',
                    'muscleRate', 'visceralFat', "Gr"]
    for item in list_mes:
        row = item.to_list()
        row.insert(0, len(result) + 1)
        result.append(row)
    return tabulate(result, headers=headers_list, tablefmt="fancy_grid")


if __name__ == '__main__':
    main()
