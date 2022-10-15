from tkinter import ttk, Label
from typing import List

from tkfontawesome import icon_to_image


class OpenFileFrame(ttk.Frame):
    labels: List[str] = ["Open the link: ",
                         "Proceed to 'Export Data'",
                         "proceed to login",
                         "You will be warned that there is the risk of data corruption",
                         "Then a mail will be sent with a link to a password-protected ZIP archive",
                         "Open the file in this app"]

    def __init__(self, parent):
        super().__init__(parent)
        self.image_open = icon_to_image("folder-open", scale_to_width=16)
        self.button_open = ttk.Button(self,
                                      text="Open File",
                                      image=self.image_open,
                                      compound="left")
        self.button_open.grid(row=5, column=1)
        link = Label(self, text="https://user.huami.com/privacy/index.html#/",
                     font=('Arial', 15),
                     fg="blue",
                     cursor="hand2")
        link.grid(row=0, column=1, padx=20, pady=10)
        y = 0
        for item in self.labels:
            Label(self,
                  text=f'{y + 1}. {item}',
                  font="arial").grid(
                row=y,
                column=0,
                sticky="w",
                padx=20,
                pady=10)
            y = y + 1
