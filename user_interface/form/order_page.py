#!venv/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
import time
from PIL import Image, ImageTk
from  user_interface.form.base import WindowBase
from user_interface.form.menu_page import MenuWindow

class OrderWindow(WindowBase):
    def __init__(self, logged_user:str=None) -> None:
        super().__init__()

        self.logged_user = logged_user
        self._setup_ui()
     
    def _setup_ui(self):
        self.window.title('Select Tables / Takeaway')
        self.window.config(bg='deep sky blue')
        self.width, self.height = self.auto_set_window_geometry(scale=0.9)
        self.__setup_scenes(image="./user_interface/media/tableselect.jpg")

        self.__logged_user_label = tk.Label(self.window, text='Logged in as ' + self.logged_user, font='bold')
        self.__logged_user_label.place(x=0, y=0)

        self.__digital_clock_label = tk.Label(self.window, font='bold')
        self.__digital_clock_label.place(x=900, y=0)
        self.__update_digital_clock()

        self.__log_out_button = tk.Button(text='Log Out', padx=5, width=10, command=self.closs_window)
        self.__log_out_button.place(x=1280, y=0)

        self.__table_panel = TablePanel(self.window, orderer=self.logged_user)
        self.__table_panel.add_dining_table(name="Table 1", column=1, row=1)
        self.__table_panel.add_dining_table(name="Table 2", column=2, row=1)
        self.__table_panel.add_dining_table(name="Table 3", column=3, row=1)
        self.__table_panel.add_dining_table(name="Table 4", column=1, row=2)
        self.__table_panel.add_dining_table(name="Table 5", column=2, row=2)
        self.__table_panel.add_dining_table(name="Table 6", column=3, row=2)
        self.__table_panel.add_dining_table(name="Takeaway", column=1, row=3, ipadx=100, columnspan=4)
        self.window.grid_columnconfigure(0, minsize=380)
        self.window.grid_rowconfigure(0, minsize=250)

    def __setup_scenes(self, image=None):
        self.scenes_width, self.scenes_height = int(self.width*0.98), int(self.height*0.9)
        x, y = int((self.width/2) - (self.scenes_width/2)), int((self.height/2) - (self.scenes_height/2))

        self.__scenes_img = Image.open(image)
        self.__scenes_img = self.__scenes_img.resize((self.scenes_width, self.scenes_height), Image.ANTIALIAS)
        self.__scenes_img = ImageTk.PhotoImage(self.__scenes_img)

        self.__scenes = tk.Label(self.window)
        self.__scenes.config(image=self.__scenes_img)
        self.__scenes.place(x=x, y=y)
        
    def __update_digital_clock(self):
        today_date = time.strftime("%m/%d/%Y")
        now_time = time.strftime("%I:%M:%S %p")
        self.__digital_clock_label.config(text=f"Date: {today_date}  Time: {now_time}")
        self.__digital_clock_label.after(1000, self.__update_digital_clock)

class TablePanel(tk.Frame):
    def __init__(self, parent=None, orderer=None):
        self.parent = parent
        self.orderer = orderer

    def add_dining_table(self, name, pady=30, padx=30, **kwargs):
        table = DiningTable(self.parent, name=name, orderer=self.orderer)
        table.grid(kwargs, pady=pady, padx=padx)

class DiningTable(tk.Button):
    STYLE = {
        "font": "arial 15 bold",
        "padx": 5,
        "pady": 5,
        "bg": "yellow",
        "width": 10
    }
    def __init__(self, parent=None, name=None, orderer=None) -> None:
        super().__init__(parent, text=name,  command=self.__pressed, **self.STYLE)
        self.bind('<Double 1>', self.__double_click)
        self.name = name
        self.orderer = orderer

    def __pressed(self):
        self.config(bg='black')
        self.configure(state=tk.DISABLED)

        self.menu_panel = MenuWindow(table=self.name, orderer=self.orderer)
        self.menu_panel.window.mainloop()

        self.config(bg='yellow')
        self.configure(state=tk.NORMAL)

    def __double_click(self, event):
        self.menu_panel.window.deiconify()
        
