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
[`/catalog/database`](/catalog/__init__.py)
we can seed the database with fake data. This is useful for testing as well as demonstration 
purposes.

The `populate_db` function will create the Item, Category and User tables 
([models.py](catalog/models.py)) and populate them with simulated data.
```
>>> from catalog.database import populate_db
>>> populate_db()
```  
> For details on the individual helper functions see the [API](#api) section.


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
