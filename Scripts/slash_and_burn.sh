#!/usr/bin/env bash

set -o errexit
set -o pipefail
[ "${DEBUG}" = 'true' ] && set -o xtrace

[ "${DEBUG}" = 'true' ] && echo "PWD = $PWD"

echo "Slashing and burning database." && { [ -f "${PWD}/db.sqlite3" ] || { echo "No database file. (${PWD}/db.sqlite3)" && false; } } && { rm $PWD/db.sqlite3 && echo "Database deleted." || echo "Database could not be deleted."; }

[ -d "${PWD}/Revitalize/migrations/" ] && echo "Deleting migrations." && { rm -r $PWD/Revitalize/migrations/ && echo "Migrations deleted." || echo "Migrations could not be deleted."; }

echo "Reinitializing database."

$PWD/manage.py makemigrations
$PWD/manage.py migrate --run-syncdb

echo "Database reinitialized. Generating admin account"

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', 'cs4820')" | python $PWD/manage.py shell

echo "Created admin account:"
echo "     username:  admin"
echo "     password:  cs4820"