from tkinter import ttk
import tkinter as tk
from typing import List

from measurement import Measurement
from measurement_file import generate_list


class ListFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame", padding=15)
        self.tree = self.create_tree_widget()

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

        tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        return tree

    def populate_treeview(self, item_list: List[Measurement]):
        for item in self.tree.get_children():
            self.tree.delete(item)
        lista = generate_list(item_list)
        for item in lista:
            self.tree.insert('', tk.END, values=item)
