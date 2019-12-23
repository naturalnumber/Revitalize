#!/usr/bin/env bash

set -o errexit
set -o pipefail
[ "${DEBUG}" = 'true' ] && set -o xtrace

pip freeze --path ./venv/lib/python3.7/site-packages/ > requirements.txt