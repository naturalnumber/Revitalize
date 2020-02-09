#!/usr/bin/env bash

set -o errexit
set -o pipefail
[ "${DEBUG}" = 'true' ] && set -o xtrace

$PWD/Scripts/slash_and_burn.sh

echo "from Revitalize.models import *; exec(open(\"${PWD}/load_surveys.py\").read())" | python $PWD/manage.py shell
