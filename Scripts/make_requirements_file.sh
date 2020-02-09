#!/usr/bin/env bash

set -o errexit
set -o pipefail
[ "${DEBUG}" = 'true' ] && set -o xtrace

read -p "Would you like to back-up your current file? Y/n " -n 1 -r
echo


if [[ ${REPLY} =~ ^[Yy]$ ]]
then
    [ -f "${PWD}/requirements.txt.backup" ] && rm $PWD/requirements.txt.backup
    [ -f "${PWD}/requirements.txt" ] && mv $PWD/requirements.txt $PWD/requirements.txt.backup
fi

pip freeze -l > $PWD/requirements.txt

echo "Requirements file updated."
head $PWD/requirements.txt