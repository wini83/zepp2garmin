import tkinter as tk
from datetime import date
from os import chdir, path
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo

import click
from dotenv import dotenv_values
from loguru import logger

from app import App

chdir(path.dirname(path.abspath(__file__)))

logger.add("zepp2garmin.log", rotation="1 week")




@click.command()
@click.option('--file_name', type=click.File('r'))
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
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
