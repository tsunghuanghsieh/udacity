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
From exercise folder, run `./setup.sh` to populate databases and `./teardown.sh` to remove databases. Also from project folder, run `./runflask.sh` to start the Flask app.

### Exercise [Bookshelf](https://github.com/tsunghuanghsieh/udacity/tree/main/nd0044/bookshelf)
[README.md](https://github.com/tsunghuanghsieh/udacity/tree/main/nd0044/bookshelf/README.md)

### Project [Trivia](https://github.com/tsunghuanghsieh/udacity/tree/main/nd0044/02_trivia_api)
From project folder, run `./setup.sh` to populate databases and `./teardown.sh` to remove databases. Also from project folder, run `./runflask.sh` to start the Flask app. From [frontend](https://github.com/tsunghuanghsieh/udacity/tree/main/nd0044/02_trivia_api/frontend) folder in another terminal, run `npm install` once to install dependencies and followed by `npm start` to start the React app.

## Identity and Access Management
For this section, you will need Python 3.7. You can run `source ./source03.sh` to set up your Python development environment and `source ./teardown03.sh` to tear down. Database used is SQLite and the database file is in [database folder](https://github.com/tsunghuanghsieh/udacity/tree/main/nd0044/03_coffee_shop_full_stack/backend/src/database). To connect to the database, run `sqlite3 [relative_path_to]/database.db`.

### Project [Coffee Shop Full Stack](https://github.com/tsunghuanghsieh/udacity/tree/main/nd0044/03_coffee_shop_full_stack)

## Server Deployment, Containerization and Testing
Install the latest [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

For this section, you will need Python 3.7. You can run `source ./source04.sh` to set up your Python development environment and `source ./teardown04.sh` to tear down.

### Project [Server Deployment and Containerization](https://github.com/tsunghuanghsieh/cd0157-Server-Deployment-and-Containerization)
From project folder, run `./setup_1_ekscluster.sh`, `./setup_2_cloudformation_stack.sh` and `./setup_3_iamrole.sh` to create EKS Cluster, CloudFormation stack, as well as role and policy on AWS. It will push a containerized Flask app to EKS. To find out external facing URI, run `kubectl get services simple-jwt-api -o wide`. Subsequent commits to the project will automatically trigger a build and push to EKS. Remember to run `./teardown_cloudformation_stack.sh` and `./teardown_ekscluster.sh` when done. AWS resources costs money.