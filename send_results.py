from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


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
