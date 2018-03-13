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
1. Navigate into the base folder.
1. Run `docker-compose up`
1. :fire::fire::fire:

1. You'll need to run migrations on the database to get it caught up.
   ```
   $> sudo docker exec -it screenplayreader_web_1 /bin/bash
   timekeeper_web_1$> python manage.py makemigrations
   timekeeper_web_1$> python manage.py migrate
   ```
1. Open your browser to [localhost][1].

### Usage

#### Importing Content
1. Visit the [Importer app API root][2].
1. Send a POST request of your content to the [ImportedContent endpoint][2.1]. 

#### Parsing Content
1. Visit the [Importer app API root][2].
1. Create a new [ParseOperation][2.2] and [run the operation][2.3]. 

#### Interpreting Content
1. Visit the [Interpreter app API root][3].
1. Create a new [InterpretOperation][3.1] and [run the operation][3.2]. 

#### Exporting Content
1. Visit the [Exporter app API root][4].
1. Navigate to a [Screenplay][4.1] created by the [Interpreter][3].
1. Download [Basics CSV][4.2] or [Character Breakout CSV][4.3].

## Structure
Django-based site with REST API framework

* `screenplayreader` - Django project
  * `importer` - Django application
  * `interpreter` - Django application
  * `exporter` - Django application

## Additional Resources
* [Writing your first Django App Tutorials][10]
* [Django REST framework Documentation][11]
* [REST API Quick Tips][12]
* [API Cheatsheet][13]


[1]: http://localhost:8000/
[2]: http://localhost:8000/importer/
[2.1]: http://localhost:8000/importer/imported-content/
[2.2]: http://localhost:8000/importer/parse-operations/
[2.3]: http://localhost:8000/importer/parse-operations/{:pk}/run-operation
[3]: http://localhost:8000/interpreter/
[3.1]: http://localhost:8000/interpreter/interpret-operations/
[3.2]: http://localhost:8000/interpreter/interpret-operations/{:pk}/run-operation
[4]: http://localhost:8000/exporter/
[4.1]: http://localhost:8000/exporter/screenplays/
[4.2]: http://localhost:8000/exporter/screenplays/{:pk}/basics-csv
[4.3]: http://localhost:8000/exporter/screenplays/{:pk}/character-csv
[10]: https://docs.djangoproject.com/en/2/intro/tutorial01/
[11]: http://www.django-rest-framework.org/
[12]: http://www.restapitutorial.com/lessons/restquicktips.html
[13]: https://github.com/RestCheatSheet/api-cheat-sheet#api-design-cheat-sheet
