RADAR API


Introduction

This API contains user authentication. 

Follow this link to read the API documentation

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

start Django server, 
py manage.py runserver

http://127.0.0.1/api/endpoint/

