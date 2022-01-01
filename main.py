#!venv/bin/python3
# -*- coding: utf-8 -*-

from user_interface.form.login_page import LoginWindow

if '__main__' == __name__:
    login_window = LoginWindow()
    login_window.window.mainloop()