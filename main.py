import time
from datetime import date
from os import chdir, path
from typing import List

import click
from dotenv import dotenv_values
from loguru import logger
from tabulate import tabulate

from app import App
from gc_adapter import GarminAdapter
from measurement import Measurement
from measurement_file import MeasurementsFile

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
@click.option("--no_gui", is_flag=True, help="Run without notifications", default=False)
def main(file_name, date_start, date_end, height, only_read, no_gui):
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
    if not no_gui:
        app = App()
        app.mainloop()
        exit()
    file_of_measurements = MeasurementsFile()
    file_of_measurements.load_from_csv(file_name)

    click.echo(f"Measurements in file:  {len(file_of_measurements.measurements)} (total)")

    file_of_measurements.filter_by_date(date_start, date_end)

    file_of_measurements.filter_by_height(height)

    click.echo(f"Measurements filtered:  {len(file_of_measurements.filtered_list)} ")

    file_of_measurements.group_by_date()

    click.echo(generate_table(file_of_measurements.filtered_list))

    while not click.confirm('Data correct?'):
        for i in range(0, file_of_measurements.groups):
            value = click.prompt(f'Enter the ID of the measurement from the Group {i + 1} you want to keep', type=int)
            # TODO: check data
            file_of_measurements.choose_from_group(value)
        click.echo(generate_table(file_of_measurements.filtered_list))

    file_of_measurements.filter_chosen()

    click.echo(generate_table(file_of_measurements.filtered_list))

    bullet_list = generate_bullet_list(
        click.prompt(f'Enter the IDs of the measurements you want to export to Garmin Connect (comma separated: ',
                     type=str))
    click.echo(bullet_list)
    gc = GarminAdapter(email=config["EMAIL"], passw=config['PASS'])
    for bullet in bullet_list:
        measurement = file_of_measurements.filtered_list[bullet - 1]
        std_out, std_err, code = gc.log_measurement(measurement)
        print(std_out)
        print(code)
    time.sleep(5.5)


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
