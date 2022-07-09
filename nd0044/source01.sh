#!/bin/zsh

ENV_NAME=fsd1

# source this file
conda create --name $ENV_NAME -y python=3.6
conda activate $ENV_NAME
pip3 install -r "`dirname $0`/01_fyyur/requirements.txt"

