# Catalog App

##### *Udacity - Full Stack Web Developer Nanodegree* 

> A simple web app showcasing flask with back-end SQLite database integration.

## Table of Contents ####################################################################
- **[Table of Contents](#table-of-contents)**
- **[Installation](#installation/requirements)**
  - [Requirements](#requirements)
  - [Install/Setup](#install/setup)
    1. [Clone the Repository](#clone-the-repository)
    1. [Install packages](#install-packages)
    1. [Start the Server](#start-the-server)
- **[Populating the Database](#populating-the-database)**
- **[URL Table](#url-table)**
- **[API](#api)**
  - [catalog/](#catalog/)
  - [database.py](#databasepy)
  - [views.py](#viewspy)
  - [api.py](#apipy)
- **[TODO](#todo)**


## Installation/Requirements ############################################################

### Requirements 

> NOTE: *requires Python 3 or later*

- [**Flask**](http://flask.pocoo.org/) v*0.12*
- [**Flask-WTF**](https://flask-wtf.readthedocs.io/en/stable/) v*0.14*
- [**Flask-Restless**](https://flask-restless.readthedocs.io/en/stable/) v*0.17*
- [**SQLAlchemy**](https://www.sqlalchemy.org/) v*1.1*
- [**Requests-Oauthlib**](https://requests-oauthlib.readthedocs.io/en/latest/) v*0.8*
- [**Mimesis**](https://lk-geimfari.github.io/mimesis/) v*1.0*


### Install/Setup #######################################################################

1. #### Clone the Repository 
    ```
    ➜ git clone https://github.com/klazich/catalog.git project
    ➜ cd project
    ```

1. #### Install Packages
    ```
    ➜ pip install Flask Flask-WTF Flask-Restless SQLAlchemy requests_oauthlib mimesis
    ```
    or with [requirements.txt](requirements.txt)...
    ```
    ➜ pip install -r requirements.txt,
    ```
    
1. #### Start the Server
    The flask app will load the "development" configs by default (see 
    [config.py](config.py)). Load different flask 
    configs by setting the `FLASK_CONFIG` environment variable to `dev`, `test`, or `prod`.
    ```
    ➜ export FLASK_CONFIG=prod
    ```
    or with a python script...
    ```
    >>> import os
    >>> os.environ['FLASK_CONFIG'] = 'prod'
    ```
    to start the server enter:
    ```
    ➜ python run.py
    ```
    then open up a browser to [http://localhost:5000/](http://localhost:5000/)
    
    
## Populating the Database ##############################################################
Using [Mimesis](https://lk-geimfari.github.io/mimesis/) and helper functions from 
[`/catalog/database`](/catalog/__init__.py) we can seed the database with fake data. This is useful for testing as 
well as demonstration purposes.

To populate all the tables in the database use `populate_db`:
  ```
  >>> from catalog.database import populate_db
  
  >>> populate_db()
  ```
  > Note: *Be aware that* `populate_db` *will call* `drop_db` *witch will drop all the database tables.*
  - **`populate_db()`** will create the Item, Category and User tables ([models.py](catalog/models.py)) and populate 
  them with simulated data using the other function is the database module. 

Use `init_db` and `drop_db` to create metadata tables and drop tables, respectively.
  ```
  >>> from catalog.database import init_db, drop_db
  
  >>> init_db()  # to create database tables 
  >>> drop_db()  # to drop all tables in database
  ```
  - **`init_db()`** will create all tables found in the metadata if they are not already created.
  - **`drop_db()`** will drop all tables in the database. 

To populate individual tables use `populate_users(n)`, `populate_categories()` and `populate_items(n)`:
  ```
  >>> from catalog.database import populate_users, populate_categories, populate_items
  
  >>> populate_users(10)     # add 10 User objects to database
  >>> populate_categories()  # add Category objects to database
  >>> populate_items(90)     # add 90 Item objects to database
  ```
  - `populate_users(n)` will create and commit `n` users to the database (defaults to `n=100`).
  - `populate_categories()` will create and commit the simulated categories.
  - `populate_items(n)` will create and commit `n` items to the database (defaults to `n=600`).


## URL Table ############################################################################

| Request URL Path       | View Function/Flask Extension   | |
| ---------------------- | ------------------------------- | --- |
| `/catalog`             | catalog.index()                 | *Renders site index, listing categories* |
| `/auth/login`          | auth.login()                    | *Renders the login page* |
| `/auth/logout`         | auth.logout()                   | *Logs out user and redirects to referrer* |
| `/auth/{provider}`     | auth.oauth2_authorize(provider) | *Initiates user authentication request to provider OAuth2 service* |
| `/auth/callback`       | auth.oauth2_callback()          | *Handles the callback from provider OAuth2 service and redirects to auth.login referrer* |
| `/category/{id}`       | category.read(id)               | *Renders a list of items from category with `id` (*extends catalog.index*)* |
| `/item/new`            | item.create()                   | *Renders the `ItemForm` for item creation* |
| `/item/{id}`           | item.read(id)                   | *Renders a summary of an item with `id` (*extends category.read*)* |
| `/item/{id}/update`    | item.update(id)                 | *Renders the `ItemForm` for item with `id` updates* |
| `/item/{id}/delete`    | item.delete(id)                 | *Removes item with `id` from database* |
| `/api/categories`      | *Flask-Restless*                | *Returns a list of all category objects in JSON format* |
| `/api/categories/{id}` | *Flask-Restless*                | *Returns an individual category object with `id` in JSON format* |
| `/api/items`           | *Flask-Restless*                | *Returns a list of all item objects in JSON format* |
| `/api/items/{id}`      | *Flask-Restless*                | *Returns an individual item object with `id` in JSON format* |*
*

## API ##################################################################################

### 


## TODO #################################################################################
  - Move the populate database functions into a cli.
