#!/bin/zsh

. "`dirname $0`/sh_common.sh"

#
# usage
#
usage() {
    echo -e usage: $MSG_ERROR_PREFIX $* 1>&2
    echo -e usage: `basename ${funcfiletrace[1]%:*}` 'flask_pyfile' 1>&2
    echo -e usage: flask_pyfile is the name of python script of the flask app 1>&2
    exit 1
}

# START
[ $# -ne 1 ] && usage "incorrect number of arguments"

if [ ! -f $1 ]; then
   echo "$1 does not exist..."
   exit 0
fi

[[ ${1##*.} != "py" ]] && usage "expects a python script"

# check if postgres server is running
if [ ! -f /usr/local/var/postgres/postmaster.pid ]; then
    # start postgres server
    pg_ctl -D /usr/local/var/postgres start -s -l "postgres_`date +%Y%m%d_%H%M%S`.log"
    echo
    formatYellow "To shut down postgres server"
    formatYellow "pg_ctl -D /usr/local/var/postgres stop -s"
    echo "\n\n"
else
   echo "postgres server is already running..."
fi

FLASK_APP=$1 FLASK_DEBUG=true flask run

