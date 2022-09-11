import csv
import os
import time
from datetime import date, timedelta
from os import chdir, path
from typing import List

import click
from loguru import logger
from tabulate import tabulate

from measurement import Measurement
from dotenv import dotenv_values

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
    config = dotenv_values(".env")
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
                filtered_list[i - 1].group = group_id
                filtered_list[i - 1].chosen = True
            filtered_list[i].group = group_id

    click.echo(generate_table(filtered_list))

    while not click.confirm('Data correct?'):
        for i in range(0, group_id):
            value = click.prompt(f'Enter the ID of the measurement from the Group {i + 1} you want to keep', type=int)
            # TODO: check data
            filtered_list[value].chosen = True
            item_id = 1
            for item in filtered_list:
                if item.group == i + 1:
                    if value != item_id:
                        item.chosen = None
                    else:
                        item.chosen = True
                item_id += 1
        click.echo(generate_table(filtered_list))

    filtered_list = list(filter(lambda x: (x.group is not None and x.chosen) or (x.group is None), filtered_list))
    for item in filtered_list:
        item.group = None
        item.chosen = None
    click.echo(generate_table(filtered_list))

    bullet_list = generate_bullet_list(
        click.prompt(f'Enter the IDs of the measurements you want to export to Garmin Connect (comma separated: ',
                     type=str))
    click.echo(bullet_list)
    for bullet in bullet_list:
        measurement = filtered_list[bullet - 1]
        if measurement.weight is not None:
            message = generate_gc_payload(config["EMAIL"], config['PASS'], measurement)
            click.echo(message)
            result = os.system(message)
            print(result)
            time.sleep(5.5)


def generate_gc_payload(email: str, passw: str, item: Measurement):
    command_path = os.path.dirname(__file__)
    message = command_path + '/bodycomposition upload '
    if item.boneMass is not None:
        message += '--bone-mass ' + "{:.2f}".format(item.boneMass) + ' '
    if item.bmi is not None:
        message += '--bmi ' + "{:.2f}".format(item.bmi) + ' '
    message += '--email ' + email + ' '
    if item.fatRate is not None:
        message += '--fat ' + "{:.2f}".format(item.fatRate) + ' '
    if item.bodyWaterRate is not None:
        message += '--hydration ' + "{:.2f}".format(item.bodyWaterRate) + ' '
    # message += '--metabolic-age ' + "{:.0f}".format(lib.getMetabolicAge()) + ' '
    if item.muscleRate is not None:
        message += '--muscle-mass ' + "{:.2f}".format(item.muscleRate) + ' '
    message += '--password ' + passw + ' '
    # message += '--physique-rating ' + "{:.2f}".format(lib.getBodyType()) + ' '
    message += '--unix-timestamp ' + int(item.timestamp.timestamp()).__str__() + ' '
    if item.visceralFat is not None:
        message += '--visceral-fat ' + "{:.2f}".format(item.visceralFat) + ' '
    if item.weight is not None:
        message += '--weight ' + "{:.2f}".format(item.weight) + ' '
    return message


def generate_table(list_mes: List[Measurement]):
    result = []
    headers_list = ["ID", 'time', 'weight', 'height', 'bmi', 'fatRate', 'bodyWaterRate', 'boneMass', 'metabolism',
                    'muscleRate', 'visceralFat', "Gr"]
    for item in list_mes:
        row = item.to_list()
        row.insert(0, len(result) + 1)
        result.append(row)
    return tabulate(result, headers=headers_list, tablefmt="fancy_grid")


def generate_bullet_list(input_str: str) -> List[int]:
    splited = input_str.split(",")
    result: List[int] = []
    # TODO:make robust
    for element in splited:
        splited2 = element.split("-")
        if len(splited2) == 1:
            result.append(int(element))
        elif len(splited2) == 2:
            for i in range(int(splited2[0]), int(splited2[1]) + 1):
                result.append(i)
        else:
            raise ValueError
    return result


if __name__ == '__main__':
    main()
