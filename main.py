import csv
from datetime import datetime, date
from typing import List

import click
from os import chdir, path
from loguru import logger

from measurement import Measurement

chdir(path.dirname(path.abspath(__file__)))

logger.add("zepp2garmin.log", rotation="1 week")


@click.command()
@click.argument('file_name', type=click.File('r'))
@click.option('--date-start', type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()))
@click.option('--date-end', type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()))
@click.option("--only_read", is_flag=True, help="Run without notifications", default=False)
def main(file_name, date_start, date_end, only_read):
    click.echo(click.style('zepp2garmin - transfer body composition from Zepp to Garmin Connect',
                           fg='black',
                           bold=True,
                           bg="yellow",
                           blink=True))
    click.echo(f'{"=" * 120}')
    logger.info("zepp2garmin - transfer body composition from Zepp to Garmin Connect")
    logger.info(f"Start: {date_start}, End: {date_end} ")
    measurements: List[Measurement] = []
    csv_reader = csv.reader(file_name, delimiter=',')
    for row in csv_reader:
        if csv_reader.line_num > 1:
            if len(row) == 10:
                item = Measurement(row)
                measurements.append(item)

    logger.info(f"Measurements in file:  {len(measurements)} (total)")


if __name__ == '__main__':
    main()
