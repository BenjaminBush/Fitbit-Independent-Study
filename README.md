# fitbit
This is a web-application that uses a Python framework to collect and store a user's Fitbit intraday data. 
Within the intraday module, routes/views.py handles all necesarry authentication using OAuth 2.0
The templates render an html page for two parts sof the OAuth 2.0 flow. templates/home.html renders a simple href link that will redirect 
the user to the Fitbit authentication page. templates/success.html is a simple page indicating if the authorization worked or not.
Finally, __init__.py creates the Flask application.
To actually collect data, you may either run the application locally, or on a platform like Heroku, by running the run_pull_user_data.py
script. The run_pull_user_data.py file contains all of the logic and steps for collecting a user's data and insereting it into a database. 
Please note that if you end up changing databases, it will be important to change how the psycopg2 cursor
connects in run_pull_user_data.py and intradaya/__init__.py.

#INSTALLATION
To be able to run the application, you must install the following items (either throug pip or easy_install):
Flask (0.10.1)
psycopg2 (2.6.1)
gunicorn (19.1.1)
requests (2.5.1)
requests-oauthlib (0.6.3)
python-dateutil (2.4.0)
fitbit (0.2.2)


