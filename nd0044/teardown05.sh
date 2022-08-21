#!/bin/zsh

ENV_NAME=fsd5

if [ -f "`dirname $0`/teardown05_heroku_inst" ]; then
    echo "Uninstalling heroku..."
    brew uninstall heroku
    rm "`dirname $0`/teardown05_heroku_inst"
fi

conda deactivate
conda env remove --name $ENV_NAME