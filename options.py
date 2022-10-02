from datetime import datetime, timedelta
from tkinter import ttk, StringVar, BooleanVar
from tkinter.ttk import Label


class OptionsFrame(ttk.Frame):
    def __init__(self, parent,
                 email: str = None,
                 passw: str = None,
                 date_start: datetime = None,
                 date_end: datetime = None,
                 height: float = None):
        super().__init__(parent, style="Card.TFrame", padding=15)

        self.height_entry = None
        self.filter_height_switch = None
        self.date_end_entry = None
        self.date_start_entry: ttk.Entry = None
        self.filter_date_switch = None
        self.height_label = None
        self.date_end_label = None
        self.date_start_label = None
        self.user_name_entry = None
        self.user_passwd_entry = None
        self.user_passwd_label = None
        self.usernameLabel = None
        self.password_var: StringVar = StringVar()
        self.user_name_var: StringVar = StringVar()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.filter_date_var: BooleanVar = BooleanVar(value=False)
        self.date_start_var: StringVar = StringVar()
        self.date_end_var: StringVar = StringVar()
        self.filter_height_var: BooleanVar = BooleanVar(value=False)
        self.height_var = StringVar()

        self.add_widgets()

        self.switch_date_changed()

        if email is not None:
            self.user_name_var.set(email)
        if passw is not None:
            self.password_var.set(passw)

        if date_start is not None:
            self.filter_date_var.set(True)
            self.date_start_var.set(date_start.strftime("%Y-%m-%d"))
            self.date_end_var.set(date_end.strftime("%Y-%m-%d"))
        else:
            self.date_end_var.set(datetime.now().strftime("%Y-%m-%d"))
            date_minus = datetime.today() - timedelta(days=7)
            self.date_start_var.set(date_minus.strftime("%Y-%m-%d"))

        if height is not None:
            self.filter_height_var.set(True)
            self.height_var.set(str(height))

        self.switch_date_changed()
        self.switch_height_changed()

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
            self,
            text="Filter by date",
            style="Switch.TCheckbutton",
            command=self.switch_date_changed,
            variable=self.filter_date_var)
        self.filter_date_switch.grid(row=2, column=1, columnspan=1, pady=10)

        self.date_start_entry = ttk.Entry(self, textvariable=self.date_start_var)
        self.date_start_entry.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="ew")

        self.date_end_entry = ttk.Entry(self, textvariable=self.date_end_var)
        self.date_end_entry.grid(row=4, column=1, padx=5, pady=(0, 10), sticky="ew")

        self.filter_height_switch = ttk.Checkbutton(
            self,
            text="Filter by height",
            style="Switch.TCheckbutton",
            variable=self.filter_height_var,
            command=self.switch_height_changed)
        self.filter_height_switch.grid(row=5, column=1, columnspan=1, pady=10)

        self.height_entry = ttk.Spinbox(self, from_=80, to=250, increment=1.0, textvariable=self.height_var)
        self.height_entry.insert(0, "180.0")
        self.height_entry.grid(row=6, column=1, padx=5, pady=10, sticky="ew")

    def switch_date_changed(self):
        is_enabled: bool = self.filter_date_var.get()
        if is_enabled:
            self.date_start_entry.config(state="active")
            self.date_start_label.config(state="active")
            self.date_end_label.config(state="active")
            self.date_end_entry.config(state="active")
        else:
            self.date_start_entry.config(state="disabled")
            self.date_start_label.config(state="disabled")
            self.date_end_label.config(state="disabled")
            self.date_end_entry.config(state="disabled")

    def switch_height_changed(self):
        is_enabled: bool = self.filter_height_var.get()
        if is_enabled:
            self.height_entry.config(state="active")
            self.height_label.config(state="active")
        else:
            self.height_entry.config(state="disabled")
            self.height_label.config(state="disabled")