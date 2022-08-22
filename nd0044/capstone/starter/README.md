# Capstone project Casting Agency

## Description
This project is used to help a casting agency to create movie and actor profiles, and manage matching between actors and movies. Users must be authorized to perform role-based requests to backend API. Authorization is enabled via Autho0, 3 roles, assistant, director and producer, are created and assigned separate permissions.

## Local Database Setup/Teardown
You should have already sourced [source05.sh](https://github.com/tsunghuanghsieh/udacity/blob/main/nd0044/source05.sh) to create a separate python environment `fsd5` in Conda.

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

### Actor Related Enpoings
```
GET /actors
```
* Retrieve a dictionary of actors
* Path Parameters: None
* Request Payload: None
* Response Payload: JSON object with a dictionary of actors' name and request status.

Sample response:
```
{
    "actors": [
        "Vin D",
        "Tom Cruise"
    ],
    "success": true
}
```

```
GET /actors/<int:actor_id>
```
* Retrieve details of an actor
* Path Parameters: actor_id (INT) actor id
* Request Payload: None
* Response Payload: JSON object with actor details and request status.

Sample response:
```
{
    "actors_detail": {
        "age": 40,
        "gender": "M",
        "id": 2,
        "name": "Paul Walker"
    },
    "success": true
}
```

```
POST /actors
```
* Create an actor
* Path Parameters: None
* Request Payload: JSON object with actor details
* Response Payload: JSON object with actor id and request status.

Sample request payload:
```
{
    "age": 40,
    "gender": "M",
    "name": "Paul Walker"
}
```
Sample response:
```
{
    "actor": 2,
    "success": true
}
```

```
PATCH /actors/<int:actor_id>
```
* Update actor details
* Path Parameters: actor_id (INT) actor id
* Request Payload: JSON object with actor details
* Response Payload: JSON object with actor id and request status.

Sample request payload:
```
{
    "age": 40,
    "gender": "M",
    "name": "Paul Walker"
}
```
Sample response:
```
{
    "success": true,
    "updated": 2
}
```

```
DELETE /actors/<int:actor_id>
```
* Delete actor
* Path Parameters: actor_id (INT) actor id
* Request Payload: None
* Response Payload: JSON object with actor id and request status.

Sample response:
```
{
    "deleted": 2,
    "success": true
}
```

### Movie Related Enpoings
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
### Audition Related Enpoings
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

For supported endpoints, please refer to [Actor Related Enpoings](#actor-related-enpoings), [Movie Related Enpoings](#movie-related-enpoings) and [Audition Related Enpoings](#audition-related-enpoings) for more details.
