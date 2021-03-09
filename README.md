# RADAR API

## INTRODUCTION
This API contains user authentication using Django RESTful API. 

## ASSUMPTIONS
This API should allow creating users, but users have to veryfy their email address before they can login, A token is sent to the user email address for verification, verified users can login using their email and password provided during registration, successful users got a message Hello(username) on their dashbord and only active users have access to the logout endpoint

## Design decision 
Using the frontend framework Vuejs, there is the register page which redirect to the login page and on login it goes to the dashboard. The dashbard have header, a side bar and the body, other functions of the application can be found on the side bar 

# How to run the application
To load in all python dependencies, go to the project directory
* pip install -r requirements.txt (Python 2), 
* pip3 install -r requirements.txt (Python 3)

### Configure Email Credentials in settings.py file
* EMAIL_USE_TLS = True
* EMAIL_HOST = 'smtp.gmail.com'
* EMAIL_HOST_USER = 'a valid email'
* EMAIL_HOST_PASSWORD = 'the email password'
* EMAIL_PORT = 587

### migrate the database, run the following command in the command prompt
py manage.py makemigrations
py manage.py migrate

### start Django server
py manage.py runserver
* use the link below for direct access to the endpoints
* http://127.0.0.1/api/endpoint/

### Limitation of implementation
not hosted online

### IDEAS FOR IMPROVEMENTS
* this API can have endpoints for forget password, 
* the API can have a login using other accounts like google and facebook accounts
* the API can have a two-factor authentication

### Test included
choose to use the test folder instead of the inbuilt test.py file so as to easily test all applications and files while building a bigger project.

### This API is also available for testing using the command 
* python manage.py test
* this is to test if the register endpoint successfully register user and send verification token to the user email address, test the login endpoint to make sure users can successfully login and make sure non existing user do not have access to our appliction if they have not verify their email adderess, and that verified users have access to login successfully


### SOME OTHER USEFUL FEATURES
* this API can have endpoints for forget password, 
* the API can have a login using other accounts like google and facebook accounts
* the API can have a two-factor authentication
