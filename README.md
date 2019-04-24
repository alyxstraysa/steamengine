# steam-engine
Spring 2019 CSE6242A Data and Visual Analytics Final Project

## Description

An interactive Steam game recommendation engine. Uses playtime data from [UCSD](https://cseweb.ucsd.edu/~jmcauley/datasets.html#steam_data) and reviews scraped from the Steam website to recommend games based on user preferences, and display the the most relevant reviews, review-generated game tags, and the relationships between games in an interactive graph-based web app.

Uses Django to serve content, and D3 to display content and allow for user interaction. Server infrastructure is generic enough to support arbitrary recommender and review retrieval systems, and database frameworks. D3 interface can be applied to any recommendation or graph-based context in a static or dynamic manner.

## Installation

#### Pre-requisites
* [Python](https://www.python.org/) &ge; 3.6.5 with pip (comes with default Python installation), or another package management system. Dependency installation instructions will be written for pip
* Modern web browser. [Google Chrome](https://www.google.com/chrome/) is recommended for best performance

#### Dependencies
* [django](https://www.djangoproject.com/) &ge; 2.2 (`pip install django`)
* [PyMySQL](https://github.com/PyMySQL/PyMySQL) &ge; 0.9.3 (`pip install PyMySQL`)
* [NumPy](http://www.numpy.org/) &ge; 1.16.2 (`pip install numpy`)

#### Download
Download the project with a [direct link](https://github.com/alyxstraysa/steamengine/archive/master.zip) to a zip file, or by cloning the project using the command
```
git clone https://github.com/alyxstraysa/steamengine.git
```

## Execution
To start the application, run the following command from the root of the project directory. If your Python 3 installation requires the command `python3`, use the second command.

```
python src/server/manage.py runserver
python3 src/server/manage.py runserver
```
After the server has started, navigate to the local address [http://127.0.0.1:8000/](http://127.0.0.1:8000/) with a web browser and the application should appear.

