# Plants

## Set up database
From `plants` folder, run `./setup.sh` which will create `plantsdb` database, `plants` table and initial mock data in the table. Rerunning the script will drop and recreate the database.

## Tear down database
From `plants` folder, run `./teardown.sh`.

## Start the flask app
From `plants` folder, run `./runflask.sh`.

## Operations
Using [Postman](https://www.postman.com/downloads/).

* HTTP GET http://localhost:5000/plants will return all plants in the `plants` table. Optional parameter `page` can be specified to return specific page of 10 plants.
* HTTP POST http://localhost:5000/plants will add a new plant to the `plants` table. Optional form data are `name`, `scientific_name`, `is_poisonous` and `primary_color`.
* HTTP GET http://localhost:5000/plants/<id> will return the plant's detail of the specified <id> if exists or 404 if not.
* HTTP DELETE http://localhost:5000/plants/<id> will delete the plant with the specified <id> if exists or 404 if not.

## Reference
[`models.py`](https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/Examples_from_plants_database/Flask-CORS-Example-1/models.py)