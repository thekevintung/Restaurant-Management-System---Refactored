#!venv/bin/python3
# -*- coding: utf-8 -*-

import abc

class ConcreteOrderRecoder(metaclass=abc.ABCMeta):
    def __init__(self, record_file=None, number=None, orderer=None, table=None,
                    customer=None, customer_phone_number=None) -> None:
        self.record_file = record_file
        self.number = number
        self.orderer = orderer
        self.table = table
        self.customer = customer
        self.customer_phone_number = customer_phone_number
  
    @abc.abstractmethod
    def update(self, updation=None):
        pass

    @abc.abstractmethod
    def finish_record(self):
        pass

    def add_record(self, new_record:str=None):
        self.__write_record_into_file(record=new_record)
    
    def __write_record_into_file(self, record:str=None):
        try:
            with open(self.record_file, 'a') as f:
                f.write(record)

        except IOError:
            print ("Could not open file, please close file!")

        except Exception as e:
            print(e)