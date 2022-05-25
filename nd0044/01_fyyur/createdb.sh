#!/bin/zsh

IS_POSTGRES_RUNNING=false

. "`dirname $0`/sh_common.sh"

#
# usage
#
usage() {
    echo -e usage: $MSG_ERROR_PREFIX $* 1>&2
    echo -e usage: `basename ${funcfiletrace[1]%:*}` 'database_name' 1>&2
    echo -e usage: database_name is the name of database to be created 1>&2
    exit 1
}

# START
[ $# -ne 1 ] && usage "incorrect number of arguments"

if [ ! -f /usr/local/bin/pg_ctl ]; then
   echo "postgres is not installed..."
   exit 0
fi

# check if postgres server is running
if [ ! -f /usr/local/var/postgres/postmaster.pid ]; then
    # start postgres server
    pg_ctl -D /usr/local/var/postgres start -s -l "postgres_`date +%Y%m%d_%H%M%S`.log"
else
   echo "postgres server is already running..."
   IS_POSTGRES_RUNNING=true
fi

dbname=$1

# check if db exists
db_found=`psql -lt | grep $dbname | cut -f 1 -d \|`

if [ -z $db_found ]; then
    # create db if not found
    createdb $dbname
else
    formatRed "Do you want to overwrite the existing database $dbname?"
    choice_no="No"
    choice_yes="Yes"
    choices=($choice_yes $choice_no)
    select target in $choices;
    do
        case $target in
            $choice_no|"")
                echo Goodbye!
                break;;
            *)
                echo "Dropping database $dbname..."
                dropdb $dbname
                echo "Creating database $dbname..."
                createdb $dbname
                break;;
        esac
    done
fi

# stop postgres server
if expr $IS_POSTGRES_RUNNING = false > /dev/null; then
    pg_ctl -D /usr/local/var/postgres -s stop
fi
