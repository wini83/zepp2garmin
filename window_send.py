import tkinter
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from typing import List

from measurement import Measurement


class ButtonFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame", padding=15)

        self.button = None
        self.columnconfigure(0, weight=1)

        self.add_widgets()

    def add_widgets(self):
        self.button = ttk.Button(self, text="Send to GC       ", )
        self.button.grid(row=1, column=0, padx=5, pady=10, sticky="ew")


def format_float(float_inp):
    if float_inp is None:
        output_str = "N/A"
    else:
        output_str = f'{float_inp:.2f}'
    return output_str

class ListFrame(ttk.Frame):
    filtered_list: List[Measurement] = None

    def __init__(self, parent, lista: List[Measurement]):
        super().__init__(parent)
        self.filtered_list = lista
        self.add_widgets()

    def generate_list(self):
        result = []
        for item in self.filtered_list:
            new_item = [item.timestamp, format_float(item.weight), format_float(item.muscleRate)]
            result.append(new_item)
        return result

    def add_widgets(self):
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.pack(side="right", fill="y")

        columns = ("time","weight","muscleRate")

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show=("headings",),
            yscrollcommand=self.scrollbar.set,
        )

        self.tree.heading('time', text='Time')
        self.tree.heading('weight', text='Weight')
        self.tree.heading('muscleRate', text='Muscle Rate')


        self.tree.column('time', width=120)
        self.tree.column('weight', width=64)
        self.tree.column('muscleRate', width=64)

        self.scrollbar.config(command=self.tree.yview)

        self.tree.pack(expand=True, fill="both")

        #self.tree.column("#0", anchor="w", width=140)
        #self.tree.column(1, anchor="w", width=100)

        lista = self.generate_list()
        for item in lista:
            self.tree.insert('', tkinter.END, values=item)


class PanedText(ttk.Frame):

    txt: ScrolledText = None

    def __init__(self, parent):
        super().__init__(parent)
        self.txt = self.add_widgets()

    def add_widgets(self):
        txt = ScrolledText(self, undo=True)
        txt['font'] = ('consolas', '12')
        txt.pack(expand=True, fill='both')
        return txt


class SendMainFrame(ttk.Frame):
    def __init__(self, parent, lista: List[Measurement]):
        super().__init__(parent, padding=15)

        for index in range(2):
            self.columnconfigure(index, weight=1)

        ListFrame(self, lista).grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        ButtonFrame(self).grid(
            row=0, column=1, padx=10, pady=(10, 0), sticky="nsew"
        )
        PanedText(self).grid(row=0, column=2, padx=10, pady=(10, 0), sticky="nsew")


class WindowSend(tkinter.Toplevel):
    filtered_list: List[Measurement]

    def __init__(self, parent, lista: List[Measurement]):
        tkinter.Toplevel.__init__(self, parent)
        self.filtered_list = lista
        # self.geometry("800x600")
        self.title("Send 2 GC..")
        self.main_frame = SendMainFrame(self, lista)
        self.main_frame.pack(expand=True, fill="both")
