#!/usr/bin/env bash

set -o errexit
set -o pipefail
[ "${DEBUG}" = 'true' ] && set -o xtrace

echo "Welcome to the Revitalize Virtual Environment Setup"
echo "Your operating system has been determined to be: acceptable :)"
read -p "Would you like to initialize the virtual environment in this directory? Y/n " -n 1 -r
echo


if [[ ${REPLY} =~ ^[Yy]$ ]]
then
    read -p "Do you have more than one version of Python 3? Y/n " -n 1 -r
    echo

    if [[ ${REPLY} =~ ^[Yy]$ ]]
    then

        python3.7 -m venv venv
        source venv/bin/activate
        python3.7 -m pip install -r requirements.txt

    else

        python3 -m venv venv
        source venv/bin/activate
        python3 -m pip install -r requirements.txt

    fi

fi