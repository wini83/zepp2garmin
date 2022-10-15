import tkinter as tk
from datetime import datetime
from queue import Queue
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror
from typing import List

import sv_ttk

from gc_adapter import GarminAdapter, FakeAdapter, QueueHandler, GarminResult
from list_frame import ListFrame
from measurement import Measurement
from measurement_file import MeasurementsFile
from options import OptionsFrame
from send_results import PanedText


class App(tk.Tk):
    file_measurements: MeasurementsFile

    def __init__(self,
                 email: str = None,
                 passw: str = None,
                 date_start: datetime = None,
                 date_end: datetime = None,
                 height=None,
                 fake: bool = None
                 ):
        super().__init__()

        if fake is None:
            self.fake: bool = False
        else:
            self.fake: bool = fake

        # dark_title_bar(self)
        self.title('Zepp2Garmin ')
        self.geometry('1024x760')

        sv_ttk.set_theme("dark")

        # self.menubar = self.create_menu()
        # self.config(menu=self.menubar)

        self.notebook = self.create_notebook()

        self.tree_frame = ListFrame(self.notebook)

        self.result_text = PanedText(self.notebook)

        self.options = OptionsFrame(self.notebook,
                                    email=email,
                                    passw=passw,
                                    date_start=date_start,
                                    date_end=date_end,
                                    height=height)

        self.notebook.add(self.tree_frame, text='Measurements')
        self.notebook.add(self.result_text, text='Transfer results')
        self.notebook.add(self.options, text="Options")

        self.status_var = tk.StringVar()
        self.status_var.set("Ready")

        self.context_menu = self.create_context_menu()

        self.tree_frame.button_send.bind("<Button-1>", self.send2gc)

        self.tree_frame.button_un_filter.bind("<Button-1>", self.un_filter)

        self.tree_frame.button_apply_filter.bind("<Button-1>", self.filter)

        self.tree_frame.tree.bind("<Button-3>", self.do_popup)

        status_bar = tk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def get_selected_indexes(self) -> List[int]:
        result = []
        current_items = self.tree_frame.tree.selection()
        for item in current_items:
            result.append(int(self.tree_frame.tree.item(item)['values'][0]))
        return result

    def promote(self):
        indexes = self.get_selected_indexes()
        if len(indexes) == 1:
            index = indexes[0]
            item: Measurement = self.file_measurements.filtered_list[index - 1]
            if item.group is not None:
                self.file_measurements.choose_from_group(index - 1)
                self.tree_frame.populate_treeview(self.file_measurements.filtered_list)
            else:
                showerror("Error", message=f'Item does not belong to a group!')
        else:
            showerror("Error", message=f'You have to select one item!')

    def filter(self,event):
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
        self.tree_frame.populate_treeview(self.file_measurements.filtered_list)

    def filter_duplicates(self):
        self.file_measurements.filter_chosen()
        self.tree_frame.populate_treeview(self.file_measurements.filtered_list)

    def un_filter(self,event):
        self.file_measurements.filtered_list = self.file_measurements.measurements
        for item in self.file_measurements.filtered_list:
            item.chosen = None
            item.group = None
        self.file_measurements.group_by_date()
        self.tree_frame.populate_treeview(self.file_measurements.filtered_list)

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

        # menubar.add_command(label="Send to GC", command=self.send2gc)

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

    def send2gc(self,event=None):
        indexes = self.get_selected_indexes()
        queue: Queue = Queue()
        export_list: List[Measurement] = []
        for index in indexes:
            item: Measurement = self.file_measurements.filtered_list[index - 1]
            export_list.append(item)
        self.notebook.select(1)
        self.result_text.txt.insert(tk.END, f"Sending {len(export_list)} items.." + '\n')
        if self.fake:
            gc_adapter = FakeAdapter(self.options.user_name_var.get(),
                                     passw=self.options.password_var.get())
        else:
            gc_adapter = GarminAdapter(self.options.user_name_var.get(),
                                       passw=self.options.password_var.get())
        handler = QueueHandler(queue=queue, adapter=gc_adapter, payload_list=export_list)

        handler.start()

        self.monitor_gc(handler)

    def monitor_gc(self, thread: QueueHandler):
        self.result_text.progress_var.set(thread.progress)
        if thread.is_alive():
            if not thread.queue.empty():
                msg: GarminResult = thread.queue.get()
                self.result_text.print_result(msg)
            self.after(100, lambda: self.monitor_gc(thread))
        else:
            while not thread.queue.empty():
                msg: GarminResult = thread.queue.get()
                self.result_text.print_result(msg)

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
        self.tree_frame.populate_treeview(self.file_measurements.filtered_list)

    def file_open_ext(self, file_name):
        self.file_measurements = MeasurementsFile()
        self.file_measurements.load_from_csv(file_name)
        self.file_measurements.group_by_date()
        self.tree_frame.populate_treeview(self.file_measurements.filtered_list)
