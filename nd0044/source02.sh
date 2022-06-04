#!/bin/zsh

ENV_NAME=fsd2

# source this file
conda create --name $ENV_NAME -y python=3.7 flask flask-cors
conda activate $ENV_NAME
pip3 install -r "`dirname $0`/requirements02.txt"

