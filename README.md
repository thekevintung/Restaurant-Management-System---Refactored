# Restaurant-Management-System Refactored
This project is the refactored of the "Restaurant Management System" that was clone from https://github.com/nkeyan11/Restaurant-Management-System.git.

The following introduction quoted from the original repository: https://github.com/nkeyan11/Restaurant-Management-System.git
Desktop app for “Restaurant Management System” using python Tkinter module. Project involves the dynamic ability to switch between tables for orders, with separate file writes for kitchen orders and final bill for the customers for the respective table orders. Database integration into local Mysql DB for storing the bill data for each order.

This project need to install MySQL and have a "restaurant" databse and a "staff" table that include [staffID, staffName, password] columns header. 

Following is the structure of the repository after refactored. You can run the main.py to let the "Restaurant Management System" working.

| +Records \
| +user_interface \
|---+form \
|-------base.py \
|-------login_page.py \
|-------menu_page.py \
|-------order_page.py \
|---+media\
|-------tableselect.jpg \
| +utils \
|----base.py \
|----mySQL.py \
|----record.py \
| main.py \
| README.md
