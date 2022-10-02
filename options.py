import tkinter
from tkinter import ttk, StringVar
from tkinter.ttk import Label


class OptionsFrame(ttk.Frame):
    def __init__(self, parent, email: str = None, passw: str = None):
        super().__init__(parent, style="Card.TFrame", padding=15)

        self.user_name_entry = None
        self.user_passwd_entry = None
        self.user_passwd_label = None
        self.usernameLabel = None
        self.password_var: StringVar = StringVar()
        self.user_name_var: StringVar = StringVar()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.add_widgets()

        if email is not None:
            self.user_name_var.set(email)
        if passw is not None:
            self.password_var.set(passw)

    def add_widgets(self):
        self.usernameLabel = Label(self, text="Garmin Connect User Name:")
        self.usernameLabel.grid(row=0, column=0)
        self.user_passwd_label = Label(self, text="Garmin Connect Password:")
        self.user_passwd_label.grid(row=1, column=0)
        self.date_start_label = Label(self, text="[Filter] Date Start:")
        self.date_start_label.grid(row=3, column=0)
        self.date_end_label = Label(self, text="[Filter] Date End:")
        self.date_end_label.grid(row=4, column=0)
        self.height_label = Label(self, text="[Filter] Height:")
        self.height_label.grid(row=6, column=0)


        self.user_name_entry = ttk.Entry(self, textvariable=self.user_name_var)
        self.user_name_entry.insert(0, "user@server.com")
        self.user_name_entry.grid(row=0, column=1, padx=5, pady=(0, 10), sticky="ew")

        self.user_passwd_entry = ttk.Entry(self, textvariable=self.password_var, show='*')
        self.user_passwd_entry.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")

        self.filter_date_switch = ttk.Checkbutton(
            self, text="Filter by date", style="Switch.TCheckbutton",)
        self.filter_date_switch.grid(row=2, column=1, columnspan=1, pady=10)

        self.date_start_entry = ttk.Entry(self)
        self.date_start_entry.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="ew")

        self.date_end_entry = ttk.Entry(self)
        self.date_end_entry.grid(row=4, column=1, padx=5, pady=(0, 10), sticky="ew")

        self.filter_height_switch = ttk.Checkbutton(
            self, text="Filter by height", style="Switch.TCheckbutton", )
        self.filter_height_switch.grid(row=5, column=1, columnspan=1, pady=10)

        self.height_entry = ttk.Spinbox(self, from_=80, to=250, increment=1)
        self.height_entry.insert(0, "180.0")
        self.height_entry.grid(row=6, column=1, padx=5, pady=10, sticky="ew")

