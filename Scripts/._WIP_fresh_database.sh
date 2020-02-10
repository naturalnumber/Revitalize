#!/usr/bin/env bash

# This is a work in progress, do not use

set -o errexit
set -o pipefail
[ "${DEBUG}" = 'true' ] && set -o xtrace

$PWD/Scripts/slash_and_burn.sh

python $PWD/load_surveys.py

# echo "from Revitalize.models import *; exec(open(\"${PWD}/load_surveys.py\").read())" | python $PWD/manage.py shell

# cat $PWD/load_surveys.py | python $PWD/manage.py shell