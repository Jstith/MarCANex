# Garbage-CAN

*A tool for CAN analysis on the Mach-E*

![logo](login.png)

## Software Stack

The front-end webpage was created using free bootstrap templates and code. The bootstrap is hosted on flask, which reads database information from a sqlite3 database file.

## Install

Install python and the necessary pip libraries.

```
pip install -r requirements.txt
```

Set the necessary flask environment variables and run flask to get Garbage-Can running on localhost:5000.

```
export PYTHONPATH="${PYTHONPATH}:/home/noah/Desktop/ARP/combined/Garbage-CAN/" (or whereever your directory is)
export FLASK_APP=.
flask run
```

## Current Features

* Secure password authentication / sessions
* List known CAN commands
* Query list for certain values
    * search strings
    * filter values
* Add/Remove/Edit commands

## Future Goals

* Send commands to CAN from app
* Craft multi-command injects
* mass database adds with CSV
