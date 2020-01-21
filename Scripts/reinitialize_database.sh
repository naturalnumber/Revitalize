#!/usr/bin/env bash

set -o errexit
set -o pipefail
#[ "${DEBUG}" = 'true' ] &&
set -o xtrace

rm -r ./Revitalize/migrations/
./manage.py makemigrations
./manage.py migrate --run-syncdb

