
import os
from sys import platform

if (platform == "linux"):
    # Heroku
    database_path = os.environ['DATABASE_URL']
elif (platform == "darwin"):
    # MacOS
    database_path = 'postgresql://zonghuan@localhost:5432/casting'

def getDbPath():
    return database_path