#!/bin/zsh

ENV_NAME=fsd5

if [[ -z `which heroku` ]]; then
    echo "Brewing heroku..."
    brew tap heroku/brew && brew install heroku
    touch "`dirname $0`/teardown05_heroku_inst"
fi

# source this file
conda create --name $ENV_NAME -y python=3.7
conda activate $ENV_NAME
pip3 install -r "`dirname $0`/capstone/starter/requirements.txt"
