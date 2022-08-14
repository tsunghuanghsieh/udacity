#!/bin/zsh

. "`dirname $0`/sh_common.sh"

#
# usage
#
usage() {
    echo -e usage: $MSG_ERROR_PREFIX $* 1>&2
    echo -e usage: `basename ${funcfiletrace[1]%:*}` 1>&2
    exit 1
}

# START
[ $# -ne 0 ] && usage "incorrect number of arguments"

# check if postgres server is running
if [ ! -f /usr/local/var/postgres/postmaster.pid ]; then
    # start postgres server
    pg_ctl -D /usr/local/var/postgres start -s -l "postgres_`date +%Y%m%d_%H%M%S`.log"
else
   echo "postgres server is already running..."
   IS_POSTGRES_RUNNING=true
fi

export DATABASE_URL='postgresql://zonghuan@localhost:5432/casting'

FLASK_APP=app FLASK_DEBUG=true flask run

# stop postgres server if we start it
if expr $IS_POSTGRES_RUNNING = false > /dev/null; then
    pg_ctl -D /usr/local/var/postgres -s stop
fi
