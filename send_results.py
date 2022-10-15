import tkinter
from tkinter import ttk

from gc_adapter import GarminResult


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
        self.txt = self.add_text_box()
        vsb = ttk.Scrollbar(self, command=self.txt.yview, orient="vertical")
        self.txt.configure(yscrollcommand=vsb.set)

        self.progress_var = tkinter.IntVar()

        self.pb = self.add_progress_bar(self.progress_var)



        self.button = ttk.Button(self, text="Abort!", style="Accent.TButton")

        self.grid_rowconfigure(0, minsize=30)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.pb.grid(row=0, column=0,sticky="ew", padx=5, pady=5)
        self.button.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        vsb.grid(row=1, column=2, sticky="ns")
        self.txt.grid(row=1, column=0, columnspan=2, sticky="nsew")

    def add_text_box(self):
        text = tkinter.Text(self, wrap="none")
        return text

    def add_progress_bar(self, var):
        pb = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='determinate',
            length=280,
            variable=var
        )
        return pb

    def print_result(self, msg: GarminResult):
        result = f'{msg.payload.timestamp} | '
        result += f'Body: {msg.payload.weight} kg | Muscle: {msg.payload.muscleRate} kg) | '
        if msg.std_out is not None and msg.std_out != '':
            result += f'Result: {msg.std_out} | '
        if msg.std_err is not None:
            result += f'Status: {msg.std_err} | '
        result = result + f'Code: {msg.code}'
        self.txt.insert(tkinter.END, result + '\n')

