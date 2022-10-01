import gc
import tkinter as tk
from datetime import datetime
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror
from typing import List

import sv_ttk

from gc_adapter import GarminAdapter
from measurement import Measurement
from measurement_file import MeasurementsFile, generate_list
from window_send import WindowSend, PanedText


class App(tk.Tk):
    file_measurements: MeasurementsFile
    gc_user_email: str
    gc_user_passw: str

    def __init__(self):
        super().__init__()

        # dark_title_bar(self)
        self.title('Zepp2Garmin ')
        self.geometry('1024x760')

        sv_ttk.set_theme("dark")

        self.menubar = self.create_menu()
        self.config(menu=self.menubar)

        self.notebook = self.create_notebook()

        self.tree = self.create_tree_widget()

        self.result_text = PanedText(self.notebook)

        self.notebook.add(self.tree, text='Input')
        self.notebook.add(self.result_text, text='Transfer')

        self.status_var = tk.StringVar()
        self.status_var.set("Ready")

        self.context_menu = self.create_context_menu()

        self.tree.bind("<Button-3>", self.do_popup)

        status_bar = tk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def get_selected_indexes(self) -> List[int]:
        result = []
        current_items = self.tree.selection()
        for item in current_items:
            result.append(int(self.tree.item(item)['values'][0]))
        return result

    def select_from_group(self):
        indexes = self.get_selected_indexes()
        if len(indexes) == 1:
            index = indexes[0]
            item: Measurement = self.file_measurements.filtered_list[index - 1]
            if item.group is not None:
                self.file_measurements.choose_from_group(index - 1)
                self.populate_treeview()
            else:
                showerror("Error", message=f'Item does not belong to a group!')
        else:
            showerror("Error", message=f'You have to select one item!')

    def filter(self):
        self.file_measurements.filter_by_height(172)
        date_start = datetime(2022, 9, 1)
        date_end = datetime(2022, 9, 11)
        self.file_measurements.filter_by_date(date_start, date_end)
        self.file_measurements.group_by_date()
        self.populate_treeview()

    def filter_ext(self, height: int, date_start, date_end):
        print(f'{height}; {date_start}; {date_end}')
        if height is not None:
            self.file_measurements.filter_by_height(height)
        if date_start is not None:
            self.file_measurements.filter_by_date(date_start, date_end)
        self.file_measurements.group_by_date()
        self.populate_treeview()

    def filter_duplicates(self):
        self.file_measurements.filter_chosen()
        self.populate_treeview()

    def un_filter(self):
        self.file_measurements.filtered_list = self.file_measurements.measurements
        for item in self.file_measurements.filtered_list:
            item.chosen = None
            item.group = None
        self.populate_treeview()

    def create_notebook(self):
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, expand=True, fill="both")
        return notebook

    def create_menu(self):
        menubar = tk.Menu(self)
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
        # create the Filter
        filter_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        filter_menu.add_command(label='Filter by..', command=self.filter)
        filter_menu.add_command(label='Filter duplicates', command=self.filter_duplicates)
        filter_menu.add_separator()
        filter_menu.add_command(label='Un filter', command=self.un_filter)

        # add the Help menu to the menubar
        menubar.add_cascade(
            label="Filter",
            menu=filter_menu
        )

        menubar.add_command(label="Send to GC", command=self.send2gc)

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
        return menubar

    def create_context_menu(self):
        m = tk.Menu(self, tearoff=0)
        m.add_command(label="Select", command=self.select_from_group)
        # m.add_command(label="Copy")
        # m.add_command(label="Paste")
        # m.add_command(label="Reload")
        # m.add_separator()
        m.add_command(label="Send to GC", command=self.send2gc)
        return m

    def send2gc(self):
        indexes = self.get_selected_indexes()
        list_2send: List[Measurement] = []
        for index in indexes:
            item: Measurement = self.file_measurements.filtered_list[index - 1]
            list_2send.append(item)
        self.notebook.select(1)
        self.result_text.txt.insert(tk.END, f"Sending {len(list_2send)} items.." + '\n')
        gc_adapter = GarminAdapter(self.gc_user_email, passw=self.gc_user_passw)
        item = list_2send[0]
        std_out, std_err, code = gc_adapter.log_measurement(list_2send[0])
        result = f'{item.timestamp} (Body: {item.weight} kg; Muscle: {item.muscleRate} kg) - '
        if std_out is not None and std_out != '':
            result = result + f'Result: {std_out}; '
        if std_err is not None:
            result = result + f'Status: {std_err}; '
        result = result + f'Code: {code}'
        self.result_text.txt.insert(tk.END, result + '\n')




    def do_popup(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def file_open(self):
        filetypes = (
            ('text files', '*.csv'),
            ('ZIP files', '*.zip')
        )
        filename = filedialog.askopenfilename(title='Open a file', filetypes=filetypes)
        self.file_measurements = MeasurementsFile()
        with open(filename, newline='') as csvfile:
            self.file_measurements.load_from_csv(csvfile)
        # showinfo("Info", message=f'Items: {len(self.file_measurements.measurements)}')
        self.populate_treeview()

    def file_open_ext(self, file_name):
        self.file_measurements = MeasurementsFile()
        self.file_measurements.load_from_csv(file_name)
        self.populate_treeview()

    def populate_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        lista = generate_list(self.file_measurements.filtered_list)
        for item in lista:
            self.tree.insert('', tk.END, values=item)
        self.status_var.set(f'Items: {len(lista)}')

    def create_tree_widget(self):
        columns = ("ID", 'time', 'weight', 'height', 'bmi', 'fatRate', 'bodyWaterRate', 'boneMass', 'metabolism',
                   'muscleRate', 'visceralFat', "Gr")
        tree = ttk.Treeview(self.notebook, columns=columns, show='headings')

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
        tree.column('time', width=115)
        tree.column('weight', width=45)
        tree.column('height', width=45)
        tree.column('bmi', width=45)
        tree.column('fatRate', width=45)
        tree.column('bodyWaterRate', width=45)
        tree.column('boneMass', width=45)
        tree.column('metabolism', width=45)
        tree.column('muscleRate', width=45)
        tree.column('visceralFat', width=45)
        tree.column('Gr', width=42)

        # tree.bind('<<TreeviewSelect>>', self.item_selected)
        tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # add a scrollbar
        # scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        # tree.configure(yscroll=scrollbar.set)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return tree
