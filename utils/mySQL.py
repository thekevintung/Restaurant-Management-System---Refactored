#!venv/bin/python3
# -*- coding: utf-8 -*-
import pymysql

class MySQLProcessor:
    def __init__(self) -> None:
        self.__db_settings = {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "@Show8418",
            "charset": "utf8"
        }

    def connect_database(self, database:str=None, table:str=None) -> None:
        try:
            db_settings = {**self.__db_settings, **{"db": database}}
            self.connection = pymysql.connect(**db_settings)
            self.database = database
            self.table = table
        except Exception as e:
            print(e)

    def get_database_table_info(self):
        try:
            with self.connection.cursor() as cursor:
                command = f"SELECT * FROM {self.database}.{self.table}"    
                cursor.execute(command)
                data = cursor.fetchall()
            return data
        except Exception as e:
            print(e)

    def insert_data_into_table(self, data:tuple=None):
        try:
            with self.connection.cursor() as cursor:
                command = f"SELECT * FROM {self.database}.{self.table}"    
                cursor.execute(command)
                field_name = [des[0] for des in cursor.description]

                command = f"INSERT INTO {self.database}.{self.table} ({','.join(field_name)}) VALUES {data}" 
                cursor.execute(command)
                self.connection.commit()
        except Exception as e:
            print(e)

    def delete_data_from_table(self, conditional:str=None):
        try:
            with self.connection.cursor() as cursor:
                command = f"DELETE FROM {self.database}.{self.table} WHERE {conditional}"
                cursor.execute(command)
                self.connection.commit()
        except Exception as e:
            print(e)