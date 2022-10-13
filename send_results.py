import tkinter
from tkinter import ttk


def format_float(float_inp):
    if float_inp is None:
        output_str = "N/A"
    else:
        output_str = f'{float_inp:.2f}'
    return output_str


class PanedText(ttk.Frame):

    txt: tkinter.Text = None

    def __init__(self, parent):
        super().__init__(parent)
        self.txt = self.add_widgets()
        vsb = ttk.Scrollbar(self, command=self.txt.yview, orient="vertical")
        self.txt.configure(yscrollcommand=vsb.set)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        vsb.grid(row=0, column=1, sticky="ns")
        self.txt.grid(row=0, column=0, sticky="nsew")

    def add_widgets(self):
        text = tkinter.Text(self, wrap="none")
        return text
