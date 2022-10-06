from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

def format_float(float_inp):
    if float_inp is None:
        output_str = "N/A"
    else:
        output_str = f'{float_inp:.2f}'
    return output_str


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
