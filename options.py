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

        self._filter_composition_switch = None
        self._height_entry = None
        self._filter_height_switch = None
        self._date_end_entry = None
        # noinspection PyTypeChecker
        self._date_start_entry: ttk.Entry = None
        self._filter_date_switch = None
        self._height_label = None
        self._date_end_label = None
        self._date_start_label = None
        self._user_name_entry = None
        self._user_passwd_entry = None
        self._user_passwd_label = None
        self._usernameLabel = None
        self.password_var: StringVar = StringVar()
        self.user_name_var: StringVar = StringVar()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.filter_date_var: BooleanVar = BooleanVar(value=False)
        self.date_start_var: StringVar = StringVar()
        self.date_end_var: StringVar = StringVar()
        self.filter_height_var: BooleanVar = BooleanVar(value=False)
        self.height_var = StringVar()
        self.filter_composition_var: BooleanVar = BooleanVar(value=False)

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
        self._usernameLabel = Label(self, text="Garmin Connect User Name:")
        self._usernameLabel.grid(row=0, column=0)
        self._user_passwd_label = Label(self, text="Garmin Connect Password:")
        self._user_passwd_label.grid(row=1, column=0)
        self._date_start_label = Label(self, text="[Filter] Date Start:")
        self._date_start_label.grid(row=3, column=0)
        self._date_end_label = Label(self, text="[Filter] Date End:")
        self._date_end_label.grid(row=4, column=0)
        self._height_label = Label(self, text="[Filter] Height:")
        self._height_label.grid(row=6, column=0)

        self._user_name_entry = ttk.Entry(self, textvariable=self.user_name_var)
        self._user_name_entry.insert(0, "user@server.com")
        self._user_name_entry.grid(row=0, column=1, padx=5, pady=(0, 10), sticky="ew")

        self._user_passwd_entry = ttk.Entry(self, textvariable=self.password_var, show='*')
        self._user_passwd_entry.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")

        self._filter_date_switch = ttk.Checkbutton(
            self,
            text="Filter by date",
            style="Switch.TCheckbutton",
            command=self.switch_date_changed,
            variable=self.filter_date_var)
        self._filter_date_switch.grid(row=2, column=1, columnspan=1, pady=10)

        self._date_start_entry = ttk.Entry(self, textvariable=self.date_start_var)
        self._date_start_entry.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="ew")

        self._date_end_entry = ttk.Entry(self, textvariable=self.date_end_var)
        self._date_end_entry.grid(row=4, column=1, padx=5, pady=(0, 10), sticky="ew")

        self._filter_height_switch = ttk.Checkbutton(
            self,
            text="Filter by height",
            style="Switch.TCheckbutton",
            variable=self.filter_height_var,
            command=self.switch_height_changed)
        self._filter_height_switch.grid(row=5, column=1, columnspan=1, pady=10)

        self._height_entry = ttk.Spinbox(self, from_=80, to=250, increment=1.0, textvariable=self.height_var)
        self._height_entry.insert(0, "180.0")
        self._height_entry.grid(row=6, column=1, padx=5, pady=10, sticky="ew")

        self._filter_composition_switch = ttk.Checkbutton(
            self,
            text="Filter only with full composition",
            style="Switch.TCheckbutton",
            variable=self.filter_composition_var)
        self._filter_composition_switch.grid(row=7, column=1, columnspan=1, pady=10)

    def switch_date_changed(self):
        is_enabled: bool = self.filter_date_var.get()
        if is_enabled:
            self._date_start_entry.config(state="active")
            self._date_start_label.config(state="active")
            self._date_end_label.config(state="active")
            self._date_end_entry.config(state="active")
        else:
            self._date_start_entry.config(state="disabled")
            self._date_start_label.config(state="disabled")
            self._date_end_label.config(state="disabled")
            self._date_end_entry.config(state="disabled")

    def switch_height_changed(self):
        is_enabled: bool = self.filter_height_var.get()
        if is_enabled:
            self._height_entry.config(state="active")
            self._height_label.config(state="active")
        else:
            self._height_entry.config(state="disabled")
            self._height_label.config(state="disabled")
