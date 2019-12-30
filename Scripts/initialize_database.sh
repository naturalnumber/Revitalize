#!/usr/bin/env bash

set -o errexit
set -o pipefail
#[ "${DEBUG}" = 'true' ] &&
set -o xtrace

#python3 manage.py createsuperuser <<<"admin\nrevitalize.upei@gmail.com\nSMCS4820\nSMCS4820\n"

spawn python3 $PWD/manage.py createsuperuser
expect \"Username*:\" {send \"admin\"; interact}

expect \"Password:\" {send \"SMCS4820\"; interact}
expect \"Password \(again\):\" {send \"SMCS4820\"; interact}
