#!/bin/zsh

ENV_NAME=fsd3

# source this file
conda create --name $ENV_NAME -y python=3.7
conda activate $ENV_NAME
pip3 install -r "`dirname $0`/03_coffee_shop_full_stack/backend/requirements.txt"
