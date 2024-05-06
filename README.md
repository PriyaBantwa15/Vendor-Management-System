Vendor Management System

First setup all things:
 - Must installed django latest version.
 - Download this folder into your system.
 - Goto the project folder in ternima.
 - To run first run "python manage.py makemigrations".
 - Then after that run "python manage.py migrate".
 - To run write command "python manage.py runserver".
 - Now click on the link provided in the terminal.
 - Browser will open so in browser, append "/admin" to the link.
 - Admin panel will open but for access username and password must have so for that goto termianl and write command "python manage.py createsuperuser" after this fill necessary data and then login to admin panel.
 - Now in urls.py file all the apis are provided for create, read, update, read specific and delete for vendor and purchaseorder.
 - To check the performance of specific vendor there is also api provided.
