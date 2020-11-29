# Casting Backend

## APP WEBLINK

[Flask-SQLAlchemy](https://castingmovie.herokuapp.com/)

https://castingmovie.herokuapp.com/

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic. The database operations are made available through the Flask command-line interface or through the Flask-Script extension.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the project directory (casting), first ensure you are working using your created virtual environment.
Navigate to `casting` after activating virtual environment

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

Since we will be using Postgres as the Database, we will need to create a database calling `casting` using the following command:

```bash
createdb casting
```

Since we will be using a Flask-Migrate tool, we will need to set up migrations as follows:

```bash
flask db init

flask db migrate

flask db upgrade
```

Note: Ensure you use migrate = Migrate(app, db) in place of create_all() in your `model.py`.

## Tasks

### Setup Auth0

1. Created a new Auth0 Account
2. Selected a unique tenant domain
3. Created a new, single page web application
4. Created a new API `(movietestapi)`
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `view:movies`
    - `edit:movie`
    - `add:movie`
    - `delete:movie`
    - `view:actors`
    - `edit:actor`
    - `add:actor`
    - `delete:actor`
    - `link:cast`
6. Create new roles for:
    - Cast Assistant-
        Can do the following:
        - `view:movies`,
        - `view:actors`
    - Manager-
        Can perform all from Cast Assitant and:
        - `edit:movie`
        - `edit:actor`
        - `add:actor`
        - `delete:actor`
    - Executive Producer-
        Can perform all from Cast Assitant and:
        - `add:movie`
        - `delete:movie`
        - `link:cast`

## API DOCUMENTATION

### List Of Endpoints

- GET '/actors'
- POST '/actors'
- PATCH '/actors/id'
- DELETE '/actors/id'
- GET '/movies'
- POST '/movies'
- PATCH '/movies/id'
- DELETE '/movies/id'
- POST '/link/'

### GET '/actors'

```bash
- Handles GET requests Returns a list of actors and what movies they are linked to.

```

### POST '/actors

```bash
- Uses POST request to add Actor and its properties to Database

- Request Arguments: json body header in the following format:
{
    "name": "Makudeni Goluchu",
    "age": 34,
    "gender": "Male"
}


```

### PATCH '/actors/id'

```bash
- This endpoint will EDIT actors with the specified actor ID.

- Request Arguments: Actor ID (int)

```

### DELETE '/actors/id'

```bash
- This endpoint will DELETE actors with the specified actor ID. This also deletes the link with the Movies associated with it where applicable.

- Request Arguments: Actor ID (int)

```

### GET '/movies'

```bash
- Handles GET requests Returns a list of movies and what actors they are linked to.

```

### POST '/movies

```bash
- Uses POST request to add Movie and its properties to Database

- Request Arguments: json body header in the following format:
{
    "title": "Revenge of the Black Ninja",
    "releasedate": 2005
}

```

### PATCH '/movies/id'

```bash
- This endpoint will EDIT movies with the specified movie ID.

- Request Arguments: Movie ID (int)

```

### DELETE '/movies/id'

```bash
- This endpoint will DELETE movies with the specified movie ID. This also deletes the link with the Actors associated with it where applicable.

- Request Arguments: Movie ID (int)


```

### POST '/link

```bash

- Uses POST request to link an Actor with a Movie to create an association in the Database

- Request Arguments: json body header in the following format:
{
    "movie_id": 1,
    "actor_id": 1
}
```

## Testing

To run the tests, I used unittest module. The test code is as shown in this file `test_api.py`. A postgres database was created with database name as `casting_test`. See command below:

```bash

dropdb casting_test
createdb casting_test

python3 test_api.py -v

```

NOTE: Be sure to delete/drop the tables in database between tests.

The following tests were conducted:
TEST 1: TEST ACCESS TO ADD ACTORS WITHOUT AUTH
TEST 2: TEST ACCESS TO ADD ACTORS WITH insufficient PERMISSION (AS CAST ASSISTANT)
TEST 3: TEST ACCESS TO ADD ACTORS WITH SUFFICIENT PERMISSION (AS CAST DIRECTOR)
TEST 4: TEST ACCESS TO VIEW ACTORS WITHOUT AUTH
TEST 5: TEST ACCESS TO VIEW ACTORS WITH SUFFICIENT PERMISSION (AS CAST ASSISTANT)
TEST 6: TEST ACCESS TO ADD MOVIES WITH INSUFFICIENT PERMISSION (AS CAST DIRECTOR)
TEST 7: TEST ACCESS TO ADD MOVIES WITH SUFFICIENT PERMISSION (AS EXECUTIVE PRODUCER)
TEST 8: TEST ACCESS TO VIEW MOVIES
TEST 9: TEST ACCESS TO LINK MOVIES TO ACTORS (AS EXECUTIVE PRODUCER)
TEST 10: TEST ACCESS TO EDIT ACTOR (AS CAST DIRECTOR)
TEST 11: TEST ACCESS TO EDIT MOVIE (AS CAST DIRECTOR)
TEST 12: TEST ACCESS TO DELETE ACTOR (AS CAST DIRECTOR) [WITH PERMISSION]
TEST 13: TEST ACCESS TO DELETE MOVIE (AS CAST DIRECTOR) [NO PERMISSION]
TEST 14: TEST ACCESS TO DELETE MOVIE (AS EXECUTIVE PRODUCER) [with PERMISSION]

### Results

See below for the results of the tests:

``` bash
$ python3 test_api.py -v
test_01_add_actor_no_auth (__main__.CastingTestCase) ... ok
test_02_add_actor_no_perm (__main__.CastingTestCase) ... ok
test_03_add_actor_with_perm (__main__.CastingTestCase) ... ok
test_04_view_actors_no_auth (__main__.CastingTestCase) ... ok
test_05_view_actors_with_perm (__main__.CastingTestCase) ... ok
test_06_add_movie_no_perm (__main__.CastingTestCase) ... ok
test_07_add_movie_with_perm (__main__.CastingTestCase) ... ok
test_08_view_movies (__main__.CastingTestCase) ... ok
test_09_actor_movie_link (__main__.CastingTestCase) ... ok
test_10_edit_actor (__main__.CastingTestCase) ... ok
test_11_edit_movie (__main__.CastingTestCase) ... ok
test_12_delete_actor_with_perm (__main__.CastingTestCase) ... ok
test_13_delete_movie_no_perm (__main__.CastingTestCase) ... ok

----------------------------------------------------------------------
Ran 13 tests in 2.143s
```

## Heroku

### SETUP

To set up Heroku CLI, go to the website and create an account.
Then install Heroku CLI using:

```bash
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
```

Confirm installation by checking version:

```bash
heroku --version
```

Then on your terminal, enter the following command to login (follow instructions):

```bash
heroku login
```

The first thing you want to do is create a new folder and move your project to it.
Note: DO NOT CHANGE ANY FILE IN THE FOLDER UNTIL YOU PUSH. MAKE SURE YOU HAVE CREATED YOUR REQ FILE BEFORE PROCEEDING (USING PIP FREEZE)
Use Heroku CLI to add your project to git by:

```bash
git init
git add .
git commit -m "My first commit"
```

Create an Heroku app using:

```bash
heroku create <app name>
```

This automatically ties the app to the heroku repo.
Confirm by entering the following command:

```bash
git remote -v
```

You should get a response like:

```bash
heroku  https://git.heroku.com/thawing-inlet-61413.git (fetch)
heroku  https://git.heroku.com/thawing-inlet-61413.git (push)
```

Next, we deploy the code by enting the following:

```bash
git push heroku master
```

If you updated your requirement file, your deploy will almost always fail. When it does, note the module that caused the failure, go to you requirements file and delete it, then run the following command.

```bash
git commit -m "Changed Req" -a
git push heroku master
```

Keep doing this until you have cleared all the errors.
Your app should be deployed and ready for use.

A good thing to do is have another terminal that has heroku logs running.
Open another terminal and enter the following:

```bash
heroku logs --tail
```

This terminal will show you what the logs are. it helps to immediately see if your app is running without going to Web browser.
