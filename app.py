import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo

from measurement_file import MeasurementsFile


class App(tk.Tk):
    file_measurements: MeasurementsFile

    def file_open(self):
        filetypes = (
            ('text files', '*.csv'),
            ('ZIP files', '*.zip')
        )
        filename = filedialog.askopenfilename(title='Open a file', filetypes=filetypes)
        self.file_measurements = MeasurementsFile()
        with open(filename, newline='') as csvfile:
            self.file_measurements.load_from_csv(csvfile)
        showinfo("Info", message=f'Items: {len(self.file_measurements.measurements)}')

    def __init__(self):
        super().__init__()

        self.title('Zepp2Garmin ')
        self.geometry('1024x760')

        menubar = tk.Menu(self)
        self.config(menu=menubar)
        # create the file_menu
        file_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        # add menu items to the File menu
        file_menu.add_command(label='Open...', command=self.file_open)
        file_menu.add_separator()

        # add Exit menu item
        file_menu.add_command(
            label='Exit',
            command=self.destroy
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

        self.tree = self.create_tree_widget()

        statusvar = tk.StringVar()
        statusvar.set("Ready")

        status_bar = tk.Label(self, textvariable=statusvar, relief=tk.SUNKEN, anchor="w")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_tree_widget(self):
        columns = ("ID", 'time', 'weight', 'height', 'bmi', 'fatRate', 'bodyWaterRate', 'boneMass', 'metabolism',
                   'muscleRate', 'visceralFat', "Gr")
        tree = ttk.Treeview(self, columns=columns, show='headings')

        # define headings
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

        # tree.bind('<<TreeviewSelect>>', self.item_selected)
        tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        # tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        return tree
