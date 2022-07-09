# [Full Stack Web Developer Nanodegree (nd0044 v2)](https://github.com/udacity/FSND)

For this class, you will need Python 3.x and [Postgres](https://formulae.brew.sh/formula/postgresql). The postgres version used is 14.2, unless otherwise stated. Instead of `virtualenv`, I use [Anaconda](https://www.anaconda.com/products/distribution) to manage separate Python environments.

## SQL and Data Modeling for the Web

### Project [FYYUR](https://github.com/tsunghuanghsieh/udacity/tree/main/nd0044/01_fyyur)
For this project, The highest version of python 3 is 3.6, I didn't find out about the lowest working version. You can use the following commands to create and activate environment `fyyur`.

```
conda create --name fyyur python=3.6
conda activate fyyur
```

In the Python 3.6 environment created earlier, from `01_fyyur` folder, run `pip install -r requirements.txt` to set up development environment, followed by `./createdb.sh fyyur` to create a database named `fyyur` in Postgres, `flask db upgrade` to create tables in database `fyyur`, and `psql -d fyyur -f ./createdata.psql` to populate initial mocked data in the database tables `artists`, `venues` and `shows`.

Once the development environment is set up, run `./runapp.sh app.py` and launch http://localhost:5000 in the browser to start the `Flask` app.

## API Development and Documentation
For this section, you will need Python 3.7. You can run `source ./source02.sh` to set up your Python development environment and `source ./teardown02.sh` to tear down.

### Exercise [Plants](https://github.com/tsunghuanghsieh/udacity/tree/main/nd0044/plants)
### Exercise [Bookshelf](https://github.com/tsunghuanghsieh/udacity/tree/main/nd0044/bookshelf)
### Project [Trivia](https://github.com/tsunghuanghsieh/udacity/tree/main/nd0044/02_trivia_api)

## Identity and Access Management
For this section, you will need Python 3.7. You can run `source ./source03.sh` to set up your Python development environment and `source ./teardown03.sh` to tear down. Database used is SQLite and the database file is in [database folder](https://github.com/tsunghuanghsieh/udacity/tree/main/nd0044/03_coffee_shop_full_stack/backend/src/database). To connect to the database, run `sqlite3 [relative_path_to]/database.db`.

### Project [Coffee Shop Full Stack](https://github.com/tsunghuanghsieh/udacity/tree/main/nd0044/03_coffee_shop_full_stack)