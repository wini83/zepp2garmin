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

        self.user_name_entry = ttk.Entry(self, textvariable=self.user_name_var)
        self.user_name_entry.insert(0, "user@server.com")
        self.user_name_entry.grid(row=0, column=1, padx=5, pady=(0, 10), sticky="ew")

        self.user_passwd_entry = ttk.Entry(self, textvariable=self.password_var, show='*')
        self.user_passwd_entry.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")

        self.spinbox = ttk.Spinbox(self, from_=0, to=100, increment=0.01)
        self.spinbox.insert(0, "3.14")
        self.spinbox.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        combo_list = ["Lorem", "Ipsum", "Dolor"]

        self.combobox = ttk.Combobox(self, values=combo_list)
        self.combobox.current(0)
        self.combobox.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

        self.readonly_combo = ttk.Combobox(self, state="readonly", values=combo_list)
        self.readonly_combo.current(1)
        self.readonly_combo.grid(row=4, column=1, padx=5, pady=10, sticky="ew")

        self.menu = tkinter.Menu(self)
        for n in range(1, 5):
            self.menu.add_command(label=f"Menu item {n}")

        self.menubutton = ttk.Menubutton(self, text="Dropdown", menu=self.menu)
        self.menubutton.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

        self.separator = ttk.Separator(self)
        self.separator.grid(row=6, column=0, pady=10, sticky="ew")

        self.button = ttk.Button(self, text="Click me!")
        self.button.grid(row=7, column=0, padx=5, pady=10, sticky="ew")

        self.accentbutton = ttk.Button(self, text=" I love it!", style="Accent.TButton")
        self.accentbutton.grid(row=7, column=0, padx=5, pady=10, sticky="ew")

        self.togglebutton = ttk.Checkbutton(self, text="Toggle me!", style="Toggle.TButton")
        self.togglebutton.grid(row=8, column=0, padx=5, pady=10, sticky="nsew")
