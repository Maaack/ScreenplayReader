# Screenplay Reader
A tool for reading files in screenplay formats and parsing their structure.

## Basic Idea
Upload a screenplay in .txt, .pdf, .fdx, and so on and get it parsed into
the different recognizable parts of a screenplay. Get the output through
the REST framework, or alternative future methods.

## How To Run
### Requirements
* docker
* docker-machine

### Setup
Navigate into the base folder and run:
`docker-compose up`

You'll need to run migrations on the database to get it caught up.
(If you'd like to have docker do this automagically - by all means)
```
$> sudo docker exec -it screenplayreader_web_1 /bin/bash
timekeeper_web_1$> python manage.py makemigrations
timekeeper_web_1$> python manage.py migrate
```

Go to `http://localhost:8000/`

## Structure
Django-based site with REST API framework

`screenplayreader` is the Django project name
`importer` is the Django project application

## Additional Resources
Writing your first Django App Tutorials: https://docs.djangoproject.com/en/1.10/intro/tutorial01/

Django REST framework Documentation: http://www.django-rest-framework.org/

API Cheatsheet: https://github.com/RestCheatSheet/api-cheat-sheet#api-design-cheat-sheet

REST API Quick Tips: http://www.restapitutorial.com/lessons/restquicktips.html
