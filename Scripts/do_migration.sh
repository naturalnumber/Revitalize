#!/usr/bin/env bash

set -o errexit
set -o pipefail
[ "${DEBUG}" = 'true' ] && set -o xtrace

python3 $PWD/manage.py makemigrations
python3 $PWD/manage.py migrate
