#!/bin/zsh

# check if postgres server is running
if [ ! -f /usr/local/var/postgres/postmaster.pid ]; then
    # start postgres server
    pg_ctl -D /usr/local/var/postgres start -s -l "postgres_`date +%Y%m%d_%H%M%S`.log"
else
   echo "postgres server is already running..."
   IS_POSTGRES_RUNNING=true
fi

psql -d postgres -f "`dirname $0`/backend/setup.sql"
psql -d bookshelf -f "`dirname $0`/backend/books.psql"
psql -d bookshelf_test -f "`dirname $0`/backend/books.psql"

# stop postgres server if we start it
if expr $IS_POSTGRES_RUNNING = false > /dev/null; then
    pg_ctl -D /usr/local/var/postgres -s stop
fi

if [ ! -d frontend/node_modules ]; then
    cd frontend;npm install
fi