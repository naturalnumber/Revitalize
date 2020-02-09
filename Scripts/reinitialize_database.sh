#!/usr/bin/env bash

set -o errexit
set -o pipefail
#[ "${DEBUG}" = 'true' ] &&
set -o xtrace

[ -d "${PWD}/Revitalize/migrations/" ] && rm -r $PWD/Revitalize/migrations/

$PWD/manage.py makemigrations
$PWD/manage.py migrate --run-syncdb

echo "Database reinitialized."