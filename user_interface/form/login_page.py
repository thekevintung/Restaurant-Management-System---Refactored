#!venv/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
from user_interface.form.base import WindowBase
from user_interface.form.order_page import OrderWindow
from utils.mySQL import MySQLProcessor

class LoginWindow(WindowBase):
    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._setup_mySQL(database="restaurant", table="staff")
        self.logged_user = None
        
    @property
    def mySQL_processor(self):
        return self.__mySQL_processor

    def _setup_ui(self):
        self.window.title('Login Page')
        self.window.config(bg='black')
        self.width, self.height = self.auto_set_window_geometry(scale=0.5)

        self.__username_label = tk.Label(self.window, text='Username', font='arial 18', bg='black', fg='white')
        self.__username_label.place(x=240, y=165)
        self.__username_entry = tk.Entry(self.window, width=30)
        self.__username_entry.place(x=400, y=172)

        self.__password_label = tk.Label(self.window, text='Password', font='arial 18', bg='black', fg='white')
        self.__password_label.place(x=240, y=200)
        self.__password_entry = tk.Entry(self.window, show='*', width=30)
        self.__password_entry.place(x=400, y=207)

        self.__login_button = tk.Button(self.window, text='Login', font='arial 15', bg='yellow', command=lambda: [self.__login_event()])
        self.__login_button.place(x=300, y=250)

    def _setup_mySQL(self, database:str=None, table:str=None):
        self.__mySQL_processor = MySQLProcessor()
        self.__mySQL_processor.connect_database(database=database, table=table)
        
    def __login_event(self):
        username = self.__username_entry.get()
        password = self.__password_entry.get()
        verify_success = self.__verify_login_info(username, password)
        if verify_success:
            self.window.destroy()
            self.__open_order_window()
           
    def __verify_login_info(self, username:str=None, password:str=None):
        table_data = self.mySQL_processor.get_database_table_info()
        correct_username = bool(len(list(filter(lambda x: username in x, table_data))))
        correct_password = bool(len(list(filter(lambda x: password in x, table_data))))

        if not correct_username:
            messagebox.showerror('Error', 'Username is not valid')
            return False

        if not correct_password:
            messagebox.showerror('Error', 'Password incorrect. Try again')
            return False

        self.logged_user = username
        # messagebox.showinfo('Showinfo', 'Password authentication succeeded')
        return True

    def __open_order_window(self):
        order_window = OrderWindow(self.logged_user)
        order_window.window.mainloop()