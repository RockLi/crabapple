#!/bin/bash

# Define some variables
PROJECT_NAME=demo-django-app
PROJECT_FOLDER=/tmp/demo

# Switch to the home folder of the project
cd $PROJECT_FOLDER

# Run the tests
python ./manage.py test
