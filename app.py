import tkinter as tk
from datetime import datetime
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror
from typing import List

import sv_ttk

from gc_adapter import GarminAdapter
from measurement import Measurement
from measurement_file import MeasurementsFile, generate_list
from options import OptionsFrame
from send_results import PanedText


class App(tk.Tk):
    file_measurements: MeasurementsFile

    def __init__(self,
                 email: str = None,
                 passw: str = None,
                 date_start: datetime = None,
                 date_end: datetime = None,
                 height=None
                 ):
        super().__init__()

        # dark_title_bar(self)
        self.title('Zepp2Garmin ')
        self.geometry('1024x760')

        sv_ttk.set_theme("dark")

        # self.menubar = self.create_menu()
        # self.config(menu=self.menubar)

        self.notebook = self.create_notebook()

        self.tree = self.create_tree_widget()

        self.result_text = PanedText(self.notebook)

        self.options = OptionsFrame(self.notebook,
                                    email=email,
                                    passw=passw,
                                    date_start=date_start,
                                    date_end=date_end,
                                    height=height)

        self.notebook.add(self.tree, text='Measurements')
        self.notebook.add(self.result_text, text='Transfer results')
        self.notebook.add(self.options, text="Options")

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

    def promote(self):
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
        self.file_measurements.filtered_list = self.file_measurements.measurements
        if self.options.filter_height_var.get():
            height = self.options.height_var.get()
            self.file_measurements.filter_by_height(float(height))
        if self.options.filter_date_var.get():
            date_start = datetime.strptime(self.options.date_start_var.get(), "%Y-%m-%d")
            date_end = datetime.strptime(self.options.date_end_var.get(), "%Y-%m-%d")
            self.file_measurements.filter_by_date(date_start, date_end)
        if self.options.filter_composition_var.get():
            self.file_measurements.filter_by_composition_available()

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
        self.file_measurements.group_by_date()
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
        m.add_command(label="Open file", command=self.file_open)
        m.add_separator()
        m.add_command(label='Apply filter', command=self.filter)
        m.add_command(label='Filter demoted', command=self.filter_duplicates)
        m.add_command(label='Reset Filter', command=self.un_filter)
        m.add_separator()

        m.add_command(label="Promote", command=self.promote)
        m.add_separator()
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
        gc_async_adapter = GarminAdapter(self.options.user_name_var.get(),
                                         passw=self.options.password_var.get())
        item = list_2send[0]
        gc_async_adapter.payload = item
        gc_async_adapter.start()
        self.monitor_gc(gc_async_adapter)

    def monitor_gc(self, thread: GarminAdapter):
        if thread.is_alive():
            self.after(200, lambda: self.monitor_gc(thread))
        else:
            std_out = thread.std_out
            std_err = thread.std_err
            code = thread.exit_code
            result = f'{thread.payload.timestamp} '
            result += f'(Body: {thread.payload.weight} kg; Muscle: {thread.payload.muscleRate} kg) - '
            if std_out is not None and std_out != '':
                result += f'Result: {std_out}; '
            if std_err is not None:
                result += f'Status: {std_err}; '
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
        self.file_measurements.group_by_date()
        self.populate_treeview()

    def file_open_ext(self, file_name):
        self.file_measurements = MeasurementsFile()
        self.file_measurements.load_from_csv(file_name)
        self.file_measurements.group_by_date()
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
