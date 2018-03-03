# Screenplay Reader
A tool for reading files in screenplay formats and parsing their structure.

## Basic Idea
Upload a screenplay in .txt, .pdf, .fdx, and so on and get it parsed into
the different recognizable parts of a screenplay. Get the output through
the REST framework, or alternative future methods.

## What does it do right now?
### Input
Takes plaintext of a screenplay, where newlines separate distinct sections
(ie. location, character, action, dialogue)

### Output
Outputs a csv of one scene per row, marking characters present.

<table>
    <tr>
        <th>Scene Number</th>
        <th>Location</th>
        <th>Character #1</th>
        <th>Character #2</th>
        <th>Character #3</th>
        <th>Character #4</th>
    </tr>
    <tr>
        <td>1</td>
        <td>Crime Scene</td>
        <td>X</td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>2</td>
        <td>Police Station</td>
        <td></td>
        <td>X</td>
        <td>X</td>
        <td></td>
    </tr>
    <tr>
        <td>3</td>
        <td>Hideout</td>
        <td></td>
        <td></td>
        <td></td>
        <td>X</td>
    </tr>
</table>


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

Go to http://localhost:8000/

From there you can visit http://0.0.0.0:8000/imported-content/, then
http://0.0.0.0:8000/parse-operations/, then
http://0.0.0.0:8000/interpret-operations/, finally
http://0.0.0.0:8000/exporter/{screenplay_id_here}/characters

## Structure
Django-based site with REST API framework

`screenplayreader` is the Django project
`importer` and `exporter` are the Django applications

## Additional Resources
Writing your first Django App Tutorials: https://docs.djangoproject.com/en/1.10/intro/tutorial01/

Django REST framework Documentation: http://www.django-rest-framework.org/

API Cheatsheet: https://github.com/RestCheatSheet/api-cheat-sheet#api-design-cheat-sheet

REST API Quick Tips: http://www.restapitutorial.com/lessons/restquicktips.html
