#!/bin/zsh

ENV_NAME=fsd4

if [ ! -f "/usr/local/bin/aws" ]; then
   echo "Please install AWS CLI prior to running this."
   exit 0
fi

if [ ! -f "/usr/local/bin/brew" ]; then
   echo "Please install brew prior to running this."
   exit 0
fi

brew tap weaveworks/tap
if [ ! -f "/usr/local/bin/eksctl" ]; then
    brew install weaveworks/tap/eksctl
else
    brew upgrade eksctl && brew link --overwrite eksctl
fi

if [ ! -f "/usr/local/bin/kubectl" ]; then
    brew install kubectl
else
    brew upgrade kubectl
fi

# source this file
conda create --name $ENV_NAME -y python=3.7
conda activate $ENV_NAME
pip3 install -r "`dirname $0`/04_server_deployment_and_containerization/requirements.txt"
