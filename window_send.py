import tkinter
from tkinter import ttk

from measurement_file import MeasurementsFile


class WindowSend(tkinter.Toplevel):
    file_measurements: MeasurementsFile

    def __init__(self, parent):
        tkinter.Toplevel.__init__(self, parent)  # wywolanie konstruktora klasy tk.Toplevel
        self.geometry("800x600")
        self.title("Send 2 GC..")  # wewnetrzny dostep do wlasnosci okna
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True)

        text = tkinter.Text(frame, wrap="none")
        vsb = ttk.Scrollbar(frame, command=text.yview, orient="vertical")
        hsb = ttk.Scrollbar(frame, command=text.xview, orient="horizontal")
        text.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        text.grid(row=0, column=0, sticky="nsew")

        self.menubar = self.create_menu()
        self.config(menu=self.menubar)

    def create_menu(self):
        menubar = tkinter.Menu(self)
        # create the file_menu

        menubar.add_command(label="Start process")
        menubar.add_command(label="Exit",command=self.destroy)
        return menubar