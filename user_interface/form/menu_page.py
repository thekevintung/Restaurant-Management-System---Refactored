#!venv/bin/python3
# -*- coding: utf-8 -*-

import time
import numpy as np
import tkinter as tk
from itertools import product
from pathlib import Path

from user_interface.form.base import WindowBase
from utils.base import ConcreteOrderRecoder
from utils.record import Bill, KitchenOrderRecoder, MenuTerminalRecoder

class MenuWindow(WindowBase):
    def __init__(self, orderer=None, table=None) -> None:
        super().__init__()
        self.orderer = orderer
        self.table = table
        self.number = time.strftime("%Y%m%d%I%M%S")

        self._setup_ui()
        self._setup_observers()
        
    def _setup_ui(self):
        self.window.title(self.table)
        self.window.config(bg='deep sky blue')
        self.auto_set_window_geometry(scale=0.9)

        self.__customer_info = tk.LabelFrame(self.window, text='Customer Details', font=('times new rommon', 18), bg='steel blue')
        self.__customer_name = CustomerInfoWidget(self.__customer_info, discription='Customer Name', default='Walk in Customer')
        self.__customer_phone = CustomerInfoWidget(self.__customer_info, discription='Phone NO', default='NA')
        self.__customer_info.place(x=0, y=0, relwidth=1)

        self.__buttons_panel = ButtonPanel(self.window)
        self.__buttons_panel.add_button(text='Hide Window', command=self.__hide_window)
        self.__buttons_panel.add_button(text='Add items', command=self.__add_items)
        self.__buttons_panel.add_button(text='Clear items', command=self.__clear_items)
        self.__buttons_panel.add_button(text='Finish', command=self.__finish_order)
        self.__buttons_panel.place(x=50, y=610)

        self.__menu_terminal = OrderTerminal(self.window)
        self.__menu_terminal.place(x=800, y=0, width=560, height=600)

        self.__menu = Menu(self.window)
        self.__menu.place(x=50, y=160)

        self.__amount_payable = tk.Label(self.window, text='Amount Payable: 0 Tax: 0.00',
                                        font=('times new rommon', 18, 'bold',), bg='white', fg='black')
        self.__amount_payable.place(x=960, y=620)

    def _setup_observers(self):
        self.order_observers = []
        records_folder = Path(Path.cwd(), 'Records')
        Path.mkdir(records_folder, exist_ok=True)

        config = {
            'orderer':self.orderer,
            'table':self.table,
            'number':self.number,
            'customer': self.__customer_name.get(),
            'customer_phone_number': self.__customer_phone.get()}

        self.bill = Bill(record_file=Path(records_folder, f'{self.number}.txt'), **config)
        self.kitchen_recoder = KitchenOrderRecoder(record_file=Path(records_folder, f'k{self.number}.txt'), **config)
        self.menu_terminal_recoder = MenuTerminalRecoder(terminal=self.__menu_terminal, **config)
        
        self.attach(self.bill)
        self.attach(self.kitchen_recoder)
        self.attach(self.menu_terminal_recoder)
        
    def __hide_window(self):
        self.window.withdraw()

    def __add_items(self):
        selected_items = self.__menu.get_selected_items()
        if selected_items:
            for item in selected_items:
                cost = item.price*item.quantity.get()
                self.bill.total_cost = self.bill.total_cost + cost

                order_info = {
                    'item': item.name, 
                    'price': item.price, 
                    'quantity': item.quantity.get(), 
                    'cost': cost
                }
                self.notify(order_info)
            self.__update_consumption(self.bill.total_cost)
            self.__clear_items()

    def __clear_items(self):
        self.__menu.reset_items()

    def __finish_order(self):
        self.notify(terminal=True)
        self.window.destroy()
        self.window.quit()
        
    def __update_consumption(self, consumption=None):
        text = f'Amount Payable: {consumption} Tax: {np.round(consumption*(1+self.bill.tax), 2)}'
        self.__amount_payable.config(text=text)

    def attach(self, observer: ConcreteOrderRecoder=None):
        self.order_observers.append(observer)

    def detach(self, observer: ConcreteOrderRecoder=None):
        self.order_observers.remove(observer)

    def notify(self, order_info:dict=None, terminal=False):
        for observer in self.order_observers:
            if terminal:
                observer.finish_record()
            else:
                observer.update(order_info)

    def closs_window(self):
        pass

class ButtonPanel(tk.Frame):
    BUTTON_STYLE = {
        'font': 'arial 15 bold',
        'padx': 5, 
        'pady': 5, 
        'bg': 'snow3', 
        'width': 10
    }
    def __init__(self, parent=None) -> None:
            super().__init__(parent, bg=parent.cget("bg"))

    def add_button(self, text=None, command=None):
        button = tk.Button(self, text=text, command=command, **self.BUTTON_STYLE)
        button.pack(side=tk.LEFT, expand=True, padx=45)

class OrderTerminal(tk.Frame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent, relief=tk.GROOVE, bd=10)
        self.bill_title = tk.Label(self, text='Bill Area', font='arial 15 bold', bd=7)
        self.bill_title.pack(fill=tk.X)
        self.scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.textarea = tk.Text(self, yscrollcommand=self.scroll_y)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_y.config(command=self.textarea.yview)
        self.textarea.pack(expand=True, fill=tk.BOTH)
        self.textarea.configure(font='arial 12 bold')

    def search_content(self, content):
        return bool(self.textarea.search(content, index=1.0, nocase=False, stopindex=tk.END))

    def print(self, content):
        self.textarea.insert(tk.END, content)

class CustomerInfoWidget(tk.Frame):
    LABEL_STYLE = {
        'font': ('times new rommon', 18)
    }

    ENTRY_STYLE = {
        'width': 15, 
        'font': 'arial 15', 
        'relief': tk.SUNKEN
    }
    def __init__(self, parent=None, discription=None, default='NA') -> None:
        super().__init__(parent, bg=parent.cget("bg"))
        self.__discription_label = tk.Label(parent, text=discription, **self.LABEL_STYLE)
        self.__discription_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.__discription = tk.StringVar(parent, value=default)
        self.__discription_entry = tk.Entry(parent, textvariable=self.__discription ,**self.ENTRY_STYLE)
        self.__discription_entry.pack(side=tk.LEFT, padx=10, pady=5)

    def get(self):
        return self.__discription.get()

class Menu(tk.Frame):
    PRODUCTS = {
        'Sweet Lassi': 40,
        'Mango Banana Lassi': 50,
        'Fruit Lassi': 55,
        'Dry fruit lassi': 60,
        'Mango Lassi': 45,
        'Mud coffee': 70,
        'Belgian coffee': 75,
        'Ferrero coffee': 90,
        'Mexican brownie': 60,
        'Chocolate fudge': 65,
        'Lava cake': 90,
        'Dryfruit sundae': 110,
        'Nutella Lychees': 100,
        'Butter Scotch fudge': 95,
        'Choco nut sundae': 105,
        'Turkish Coffee': 50
    }
        
    def __init__(self, parent=None) -> None:
        super().__init__(parent, bg=parent.cget("bg"))
        self.split_columns = 2

        try:
            self.menu_items = self.__create_product_items(self.PRODUCTS)
            self.__add_items_into_menu(self.menu_items)
        except Exception as e:
            print(e)

    def __create_product_items(self, products:dict=None):
        product_items = []
        for name, price in products.items():
            product_items.append(ProductWidget(self, name=name, price=price))
        return product_items

    def __add_items_into_menu(self, items:list=None):
        rows = int(np.ceil(len(items)/self.split_columns))
        columns = self.split_columns

        self.items_position = product(range(columns), range(rows))
        for item, position in zip(items, self.items_position):
            column, row = position
            item.grid(column=column, row=row, padx=25)

    def get_selected_items(self):
        selected_items = []
        for item in self.menu_items:
            if item.chkValue.get():
                selected_items.append(item)

        return selected_items

    def reset_items(self):
        for item in self.menu_items:
            item.reset()
                        
class ProductWidget(tk.Frame):
    def __init__(self, parent=None, name=None, price=None) -> None:
        super().__init__(parent, bg=parent.cget("bg"))
        self.name = name
        self.price = price
    
        self.chkValue = tk.BooleanVar(self)
        self.chkValue.set(False)
        self.check_button = tk.Checkbutton(self, text=name, variable=self.chkValue, 
                                           onvalue=40, height=2, width=20)
        self.check_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

        self.quantity = tk.IntVar(self, value=0)
        self.spin_box = tk.Spinbox(self, from_=1, to=20, width=5, textvariable=self.quantity)
        self.spin_box.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

    def reset(self):
        self.chkValue.set(False)
        self.check_button.config(variable=self.chkValue)

        self.quantity.set(1)
        self.spin_box.config(textvariable=self.quantity)