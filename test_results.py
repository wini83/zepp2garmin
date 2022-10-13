import tkinter
from datetime import datetime
from tkinter import ttk

import sv_ttk


from measurement import Measurement



class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        for index in range(2):
            self.columnconfigure(index, weight=1)
            self.rowconfigure(index, weight=1)

        measurement_item = Measurement()
        measurement_item.height = 182.0
        measurement_item.weight = 63.0
        measurement_item.muscleRate = 51.0
        measurement_item.visceralFat = 6.0
        measurement_item.timestamp = datetime.today()
        measurement_item.bodyWaterRate = 69.0
        measurement_item.fatRate = 13.0
        measurement_item.metabolism = 1380.0
        measurement_item.bmi = 66.1



def main():
    root = tkinter.Tk()
    # dark_title_bar(self)
    root.title('Zepp2Garmin ')
    root.geometry('800x600')

    sv_ttk.set_theme("dark")

    App(root).pack(expand=True, fill="both")

    root.mainloop()


if __name__ == "__main__":
    main()
