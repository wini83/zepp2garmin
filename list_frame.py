from tkinter import ttk
import tkinter as tk
from typing import List

from measurement import Measurement
from measurement_file import generate_list
from tkfontawesome import icon_to_image


class ListFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame")
        self.tree = self.create_tree_widget()
        vsb = ttk.Scrollbar(self, command=self.tree.yview, orient="vertical")
        self.tree.configure(yscrollcommand=vsb.set)
        self.image_filter = icon_to_image("filter", scale_to_width=16)
        self.image_un_filter = icon_to_image("times-circle", scale_to_width=16)
        self.image_send = icon_to_image("paper-plane", scale_to_width=16)
        self.button_apply_filter = ttk.Button(self,
                                              text="Apply Filter",
                                              image=self.image_filter,
                                              compound="left")

        self.button_un_filter = ttk.Button(self,
                                           text="Un-filter",
                                           image=self.image_un_filter,
                                           compound="left")
        self.button_send = ttk.Button(self,
                                      text="Send To Garmin Connect",
                                      style="Accent.TButton",
                                      image=self.image_send,
                                      compound="left"
                                      )
        self.grid_rowconfigure(0, minsize=30)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.tree.grid(row=1, column=0, columnspan=4, sticky="nsew")
        vsb.grid(row=1, column=5, sticky="ns")
        self.button_apply_filter.grid(row=0, column=1, pady=5, padx=5)
        self.button_un_filter.grid(row=0, column=2, pady=5, padx=5)
        self.button_send.grid(row=0, column=3, columnspan=3, pady=5, padx=5)

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

        return tree

    def populate_treeview(self, item_list: List[Measurement]):
        for item in self.tree.get_children():
            self.tree.delete(item)
        lista = generate_list(item_list)
        for item in lista:
            self.tree.insert('', tk.END, values=item)
