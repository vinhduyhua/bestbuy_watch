Web application that keep track of Bestbuy items
=======
BESTBUY WATCH

Description: Simple web application that allows user to search and keep track of the availability and prices of the Bestbuy's items

Front-end: Javacript + HTML + CSS
Back-end: Python + Django + Beautifulsoup + django-background-tasks

The application is power by Django framework that handle the dynamic of the application and the data structure of users and item's informations.
Data was extracted from Bestbuy website's HTML and Javascript tags by using "Beautifulsoup" and "requests" library.
Those data are then recorded to the Django database.
Javascript was used to fetch data from Django's database as well as POST user's input.
Because the main purpose of the app is to show the user the change in price and availability of certain items, the web scraper needs to be updated daily.
This feature was achieved by using "django-background-tasks" which runs the web scraper on the background while allowing it to be repeated at a set interval.
The front end is design with a simplicity in mind. It has the intuitive inteface with friendly color schemes and modern font-family.

To run this app [Beautifulsoup, requests, django-background-tasks] libraries are needed.
