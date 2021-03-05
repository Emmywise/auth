RADAR API


Introduction

This API contains user authentication. 

This API is also available for testing through this link http://localhost:8000/ v1

Quick Start

To load in all python dependencies
for (Python 2), pip install -r requirements.txt 
pip3 install -r requirements.txt (Python 3)


Configure Email Credentials in settings.py file

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'a valid email'
EMAIL_HOST_PASSWORD = '(the email password)'
EMAIL_PORT = 587

migrate the database, run the following command in the command prompt
py manage.py makemigrations
py manage.py migrate

start Django server, use
py manage.py runserver

http://127.0.0.1/api/endpoint/

Test included
the test is to make sure users can register, users can successfully login and make sure non existing user do not have access to our appliction if they have not verify their email adderess, and that verified users have access to login successfully

to run the test, use
python manage.py test


