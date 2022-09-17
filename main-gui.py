import tkinter as tk
from datetime import date
from os import chdir, path
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo

import click
from dotenv import dotenv_values
from loguru import logger

from measurement_file import MeasurementsFile

chdir(path.dirname(path.abspath(__file__)))

logger.add("zepp2garmin.log", rotation="1 week")
root = tk.Tk()
root.title('Zepp2Garmin ')
root.geometry('1024x760')

columns = ("ID", 'time', 'weight', 'height', 'bmi', 'fatRate', 'bodyWaterRate', 'boneMass', 'metabolism',
           'muscleRate', 'visceralFat', "Gr")

statusbar = ttk.Label(root, text="on the way…", relief=tk.SUNKEN, anchor=tk.W)

tree = ttk.Treeview(root, columns=columns, show='headings')

statusvar = tk.StringVar()
statusvar.set("Ready")

sbar = tk.Label(root, textvariable=statusvar, relief=tk.SUNKEN, anchor="w")
sbar.pack(side=tk.BOTTOM, fill=tk.X)

menubar = tk.Menu(root)
root.config(menu=menubar)
# create the file_menu
file_menu = tk.Menu(
    menubar,
    tearoff=0
)

file_measurements = None

def file_open():
    filetypes = (
        ('text files', '*.csv'),
        ('ZIP files', '*.zip')
    )
    filename = filedialog.askopenfilename(title='Open a file', filetypes=filetypes)
    file_measurements = MeasurementsFile()
    with open(filename, newline='') as csvfile:
        file_measurements.load_from_csv(csvfile)
    showinfo("Info", message=f'Items: {len(file_measurements.measurements)}')




# add menu items to the File menu
file_menu.add_command(label='Open...', command=file_open)
file_menu.add_separator()

# add Exit menu item
file_menu.add_command(
    label='Exit',
    command=root.destroy
)

# add the File menu to the menubar
menubar.add_cascade(
    label="File",
    menu=file_menu
)
# create the Help menu
help_menu = tk.Menu(
    menubar,
    tearoff=0
)

help_menu.add_command(label='Welcome')
help_menu.add_command(label='About...')

# add the Help menu to the menubar
menubar.add_cascade(
    label="Help",
    menu=help_menu
)

tree.heading('ID', text='ID')
tree.heading('time', text='Time')
tree.heading('weight', text='Weight')
tree.heading('height', text='Height')
tree.heading('bmi', text='bmi')
tree.heading('fatRate', text='Fat Rate')
tree.heading('bodyWaterRate', text='Body Water')
tree.heading('boneMass', text='Bone Mass')
tree.heading('metabolism', text='Metabolism')
tree.heading('muscleRate', text='Muscle Rate')
tree.heading('visceralFat', text='Visceral Fat')
tree.heading('Gr', text='Group')

tree.column('ID', width=20)
tree.column('time', width=120)
tree.column('weight', width=64)
tree.column('height', width=64)
tree.column('bmi', width=64)
tree.column('fatRate', width=64)
tree.column('bodyWaterRate', width=64)
tree.column('boneMass', width=64)
tree.column('metabolism', width=84)
tree.column('muscleRate', width=64)
tree.column('visceralFat', width=84)
tree.column('Gr', width=42)

tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


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
    root.mainloop()


def item_selected():
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        record = item['values']
        # show a message
        showinfo(title='Information', message=','.join(record))


if __name__ == '__main__':
    main()
