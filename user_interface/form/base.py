#!venv/bin/python3
# -*- coding: utf-8 -*-

import abc
import tkinter as tk

class WindowBase(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.__window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.closs_window)

    @property
    def window(self):
        return self.__window

    @abc.abstractmethod
    def _setup_ui(self):
        pass

    def auto_set_window_geometry(self, scale:float=1):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        self.width = int(screen_width*scale)
        self.height = int(screen_height*scale)

        x = int((screen_width/2) - (self.width/2))
        y = int((screen_height/2) - (self.height/2))

        self.window.geometry("{}x{}+{}+{}".format(self.width, self.height, x, y))
        self.window.resizable(width=0, height=0)

    def get_size(self, widget:tk.Tk=None):
        self.window.update()
        return widget.winfo_width(), widget.winfo_height()

    def closs_window(self):
        self.window.destroy()
        quit()