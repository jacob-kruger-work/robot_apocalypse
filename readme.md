[readme.md](https://github.com/jacob-kruger-work/robot_apocalypse/files/9549278/readme.md)
Robot apocalypse RESTFul API of sorts
-------------------------------------

This offers ability to add new survivor records, including their inventory and GPS coordinates, along with the ID number to identify them later on.

Will explain various relative URL paths below, along with data requests they can handle. But initially will explain file structures in terms of the django web-framework project.

### File structures

Under this repo you will find requirements.txt, which will help you configure your python virtual environment - pip install -r requirements.txt - I was working on this using python 3.9.5

Then, inside robot\_apocalypse, the following folders are specifically relevant:  

*   database - contains both the sqlite3 .db file, which the whole project operates off of, as well as a python script file called create\_database.py, which would otherwise create the database file, and generate table data structures, as well as populating the initial robots database from either a remote source, or else, if that fails, local robots.json.
*   logs - this contains another sqlite3 database that I use to save exception history in so that, if the site is running remotely, or invisibly, I can still track down errors/exceptions etc. later on.
*   static - this is just a placeholder, for now since the static path gets referred to in the main project settings.py file.?
*   testing - this folder contains my own command line test.py script to allow you to run test requests against project when it's running - simple, but, just a basic test, in case.
*   robot\_apocalypse - main project folder, with all source code under it -
    *   actions - folder contains sub-modules for robots and survivors, each containing functions that get made use of to work with data, logic, interaction, etc. in those contexts - main actual logic in these files, with forms of commenting included in all code blocks.
    *   apocalypse\_models.py - this file is a slightly tweaked version of something generated using the sqlacodegen module, which generates ORM data models to then be used when working with sqlalchemy to handle data processing.
    *   db.py - this offers basic connection - engine and session initialisation, as well as a couple of otehr functions use at times when processing data for both input and output.
    *   settings.py - the standard django settings configuration, but, tweak it slightly to include soem of my own ifno.
    *   sql\_log.py - my code to handle logging un-read exception data to an sqlite3 database, for later review.
    *   urls.py - standard django file that contains the urlpatterns collection, specifying relative paths to interact with specific pieces of code.
    *   views.py - most of the interaction processing code is included in this file, which processes input data, reroutes it to code under .actions/, etc. and then responds to client with various forms of output.

### URLs that have been specified

These URLs are specified in the urlpatterns collection inside urls.py.  

*   robots - targets views.list\_robots - just renders output of all robot entries in database.
*   survivors - also just renders output of all survivor data, but, including a dict as primary output, which then contains key-value pairs for numbers, percentages, etc., as well as different lists of survivor records, which are then rendering as dicts, with relative data included in all of them.
*   add - routes to views.add\_survivor function, which takes following arguments to then process insertion of a survivor record into database:
    *   name - required, plain string value
    *   age - simple integer value
    *   gender - simple string value
    *   id\_number - string value, required and used later on to identify survivor - must be unique
    *   latitude - floating point value
    *   longitude - floating point value
    *   inventory - string value processed from format of item|number||item2|number2||...
*   flag - used to flag a survivor as possibly infected, routing post request to views.flag\_survivor - and requires following two values:
    *   reporting - ID number of survivor reporting another as infected.
    *   infected - ID number of survivor being reported as infected - 3 flaggings will then mark a survivor as definitely having been infected.
*   gps - allows a survivor to update their current GPS coordinates - following values/arguments are made use of, and this is processed by views.gps\_coordinates:
    *   id\_number - ID number to identify which primary record to update.
    *   latitude - floating point value.
    *   longitude - floating point value.
    ### Running django project
    Once you have activated your virtual environment, from command line, in main robot_apocalypse folder, the following command will fire up the django RESTFul API listening on port 8000 by default: python manage.py runserver</div>
