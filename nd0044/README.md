# [Full Stack Web Developer Nanodegree (nd0044 v2)](https://github.com/udacity/FSND)



## [FYYUR](https://github.com/tsunghuanghsieh/udacity/tree/main/nd0044/01_fyyur)
For this project, you will need Python 3 and [Postgres](https://formulae.brew.sh/formula/postgresql). The postgres version used in 14.2. The highest version of python 3 is 3.6, I didn't find out about the lowest working version. Instead of `virtualenv`, I use [Anaconda](https://www.anaconda.com/products/distribution) to manage separate Python environments. You can use the following commands to create and activate environment `fyyur`.

`conda create --name fyyur python=3.6`

`conda activate fyyur`

In the Python 3.6 environment created earlier, from `01_fyyur` folder, run `pip install -r requirements.txt` to set up development environment, followed by `./createdb.sh fyyur` to create a database named `fyyur` in Postgres, `flask db upgrade` to create tables in database `fyyur`, and `psql -d fyyur -f ./createdata.psql` to populate initial mocked data in the database tables `artists`, `venues` and `shows`.

Once the development environment is set up, run `./runapp.sh app.py` and launch `http://localhost:5000` in the browser to start the `Flask` app.
