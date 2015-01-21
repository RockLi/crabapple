#!/bin/bash

# Define some variables
PROJECT_NAME=demo-django-app
PROJECT_FOLDER=/tmp/demo

# Switch to the home folder of the project
cd $PROJECT_FOLDER

# Scrap temporary changes

pwd

#git reset --hard
#git pull origin master

# Stop the applications
killall -9 gunicorn

# Start gunicorn
gunicorn -D -w4 --access-logfil=access.log $PROJECT_NAME.wsgi
