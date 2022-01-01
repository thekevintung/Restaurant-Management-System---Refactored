#!venv/bin/python3
# -*- coding: utf-8 -*-

import time
from  utils.base import ConcreteOrderRecoder

class Bill(ConcreteOrderRecoder):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.total_cost = 0
        self.tax = 0.05

        self.header_info =  f'                  The Lassi Corner \n' \
                            f'                      K.K.Nagar \n' \
                            f'                  Ph: 9852415687 \n' \
                            f'                  Staffname: {self.orderer}  \n       ' \
                            f'     Date/Time: {time.strftime("%d,%b,%Y / %I:%M:%S %p")}' \
                            f'\n            Bill Number: {self.number}' \
                            f'\n                     {self.table}\n' \
                            f'Order time: {time.strftime("%I:%M:%S %p")}\n' \
                            f'Order Details for {self.table} : \n' \
                            f'\n=======================================================================' \
                            f'\n  Product\t\t\t Price\t\t QTY \t Total' \
                            f'\n======================================================================='
        self.add_record(self.header_info)

    def update(self, order_info:dict=None):
        update_record = f'\n{order_info["item"]}\t\t\t {order_info["price"]}\t\t {order_info["quantity"]} \t {order_info["cost"]}'
        self.add_record(update_record)

    def finish_record(self):
        record =f'\n=======================================================================' \
                f'\n\n        Total Amount = {self.total_cost} + 5% GST({self.total_cost * self.tax})' \
                f'\n\n                Total Amount= {self.total_cost*(1+self.tax)}' \
                f'\n\n               Thank You! Visit Again!!'

        self.add_record(record)

class KitchenOrderRecoder(ConcreteOrderRecoder):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.header_info =  f'{self.table}\n' \
                            f'Order time: {time.strftime("%I:%M:%S %p")}\n' \
                            f'Order Details for {self.table} : \n'
        self.add_record(self.header_info)
 
    def update(self, order_info:dict=None):
        update_record = f'\n{order_info["item"]}\t{order_info["quantity"]}'
        self.add_record(update_record)
        
    def finish_record(self):
        record =f'\n\n\n***** Order closed for {self.number} *******'
        self.add_record(record)

class MenuTerminalRecoder(ConcreteOrderRecoder):
    def __init__(self, terminal=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.terminal = terminal
        self.header_info =  f'Bill Number: {self.number}'\
                            f'\n Customer Name:\t\t{self.customer}' \
                            f'\n Phone Number:\t\t{self.customer_phone_number}' \
                            f'\n Date / Time: {time.strftime("%d,%B,%Y / %I:%M:%S %p")}\t\t' \
                            f'\n======================================================' \
                            f'\n Product\t\t\t Price\t\t QTY \t Total' \
                            f'\n======================================================\n'

    def update(self, order_info:dict=None):
        update_record = f'\n{order_info["item"]}\t\t\t{order_info["price"]}\t\t{order_info["quantity"]}\t{order_info["cost"]}'

        if not self.terminal.search_content('Bill Number'):
            update_record = self.header_info  + '\n' + update_record

        self.terminal.print(update_record)
        
    def finish_record(self):
        pass