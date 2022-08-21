# Capstone project Casting Agency

## Local Database Setup/Teardown
You should have already sourced (source05.sh)[https://github.com/tsunghuanghsieh/udacity/blob/main/nd0044/source05.sh] to create a separate python environment `fsd5` in Conda.

From project folder, you can either run `./setup.sh` which will execute `./setup_create_db.psql`, `./setup_create_tbl.psql` and `./setup_populate_tbd.psql` to create and populate necessary database, tables and initial data. Alternatively, you can manually execute the scripts as follows. The local database is for developement and testing.
```
psql -d postgres -f ./setup_create_db.psql
psql -d casting -f ./setup_create_tbl.psql
psql -d casting -f ./setup_populate_tbd.psql
```

To tear down the database, run `./teardown.sh`.

## Third Party Tools Requirements
### Auth0
Go to [Auth0](https://auth0.com) and create an account (my personal work-related email address).

* Create a [tenant](https://manage.auth0.com/dashboard/us/fsdcapstone/) `fsdcapstone`.
* Create an [Application](https://manage.auth0.com/dashboard/us/fsdcapstone/applications) for Regular Web Application, and update necessary settings.
* Create an [API](https://manage.auth0.com/dashboard/us/fsdcapstone/apis), update necessary settings, and add the following permissions.
```
    get:actors
    get:auditions
    get:movies
    post:actors
    post:auditions
    post:movies
    patch:actors
    patch:auditions
    patch:movies
    delete:actors
    delete:auditions
    delete:movies
```
* Create roles for Assistant, Director and Producer with the following permissions.
Assistant will have the following permissions.
```
    get:actors
    get:auditions
    get:movies
```

Director  will have the following permissions.
```
    get:actors
    get:auditions
    get:movies
    post:actors
    post:auditions
    patch:actors
    patch:auditions
    patch:movies
    delete:actors
    delete:auditions
```

Producer will have the following permissions.
```
    get:actors
    get:auditions
    get:movies
    post:actors
    post:auditions
    post:movies
    patch:actors
    patch:auditions
    patch:movies
    delete:actors
    delete:auditions
    delete:movies
```
* Create a [user](https://manage.auth0.com/dashboard/us/fsdcapstone/users) and assign appropriate role.
* Using [this](https://fsdcapstone.us.auth0.com/authorize?audience=casting&response_type=token&client_id=V1zx5CXaQQGY3CZI0V8Pk8HXU8NuC8qN&redirect_uri=http://127.0.0.1:8080/login-results) to sign into the user and obtain JWT token on a browser.

### Heroku Setup
Go to [Heroku](https://signup.heroku.com/) and create an account. [Create](https://dashboard.heroku.com/new-app) a new app `boloh-capstone`. This is required for [Heroku Deployment](#heroku-deployment).

## Local Run
From the project folder, run `./runflask.sh`. The backend runs on http://127.0.0.1:5000/.

```
POST /actors
GET /actors
GET /actors/<int:actor_id>
DELETE /actors/<int:actor_id>
PATCH /actors/<int:actor_id>
```
For POST and PATCH, it requires the following JSON object in the request body.
```
{
    "name": "Actor Name",
    "age" : actor_age,
    "gender": "Actor Gender"
}
```

```
POST /movies
GET /movies
GET /movies/<int:movie_id>
DELETE /movies/<int:movie_id>
PATCH /movies/<int:movie_id>
```
For POST and PATCH, it requires the following JSON object in the request body.
```
{
    "title": "Movie Title",
    "release_date": "Release Date"
}
```

```
POST /auditions
GET /auditions
GET /auditions/<int:audition_id>
DELETE /auditions/<int:audition_id>
PATCH /auditions/<int:audition_id>
```
For POST and PATCH, it requires the following JSON object in the request body.
```
{
    "actor_id": actor_id_in_actors_table,
    "movie_id" : movie_id_in_movies_table
}
```


## Unit Testing
To run unit tests on all endpoints for RBAC, from project folder run `python3 ./test_app.py`. It mocks Auth0 JWT tokens.

## Heroku Deployment
To deploy to Heroku, sign in using `heroku login -i` first and from project folder run `./deploy_heroku.sh` to deploy to https://boloh-capstone.herokuapp.com/

Supported endpoints with GET, POST, PATCH and DELETE.
```
/actors
/auditions
/movies
```