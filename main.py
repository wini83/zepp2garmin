import sys
from datetime import date
from os import chdir, path

import click
from loguru import logger

from app import App

chdir(path.dirname(path.abspath(__file__)))

logger.add("zepp2garmin.log", rotation="1 week")


@click.command()
@click.option('--file_name', type=click.File('r'))
@click.option('--date-start', type=click.DateTime(formats=["%Y-%m-%d"]), default=None)
@click.option('--date-end', type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()))
@click.option('--height', type=int, default=None)
@click.option('--email', type=str, default=None)
@click.option('--passw', type=str, default=None)
def main(file_name, date_start, date_end, height, email, passw):
    click.echo("")
    click.echo(click.style('zepp2garmin - transfer body composition from Zepp to Garmin Connect',
                           fg='black',
                           bold=True,
                           bg="yellow",
                           blink=True))
    click.echo(f'{"=" * 120}')
    click.echo(f"Start: {date_start}, End: {date_end} ")
    app = App(email=email, passw=passw)
    if file_name is not None:
        app.file_open_ext(file_name)
    if height is not None or date_start is not None:
        app.filter_ext(height, date_start, date_end)
    app.mainloop()
    sys.exit()


if __name__ == '__main__':
    main()
