#!/bin/zsh

HEROKU_GIT_FOLDER="`dirname $0`/../../../../herokugit"
HEROKU_GIT_URL="https://git.heroku.com/boloh-capstone.git"

if [[ ! -d "$HEROKU_GIT_FOLDER" ]]; then
    echo "Creating folder for heroku deployment..."
    mkdir $HEROKU_GIT_FOLDER
else
    echo "Copying latest files for heroku deployment..."
    cp -r * $HEROKU_GIT_FOLDER
fi

cd $HEROKU_GIT_FOLDER
pwd

# set up heroku git url for the first time
if [[ -z `git remote -v 2> /dev/null | grep heroku` ]]; then
    echo "Initializing git repo..."
    git init -q
    echo "Adding git remote url to local repo..."
    git remote add heroku $HEROKU_GIT_URL
fi

git add .
git commit -m "`date +%Y%m%d_%H%M%S`"
git push heroku master