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
        echo "Proceeding with python3.7: `python3.7 --version`"
        python3.7 -m venv venv
    else
        echo "Proceeding with python3: `python3 --version`"
        python3 -m venv venv
    fi
    source venv/bin/activate
    python -m pip install -r requirements.txt
    echo "Current environment is: `python --version`"
    echo ""

    echo "Remember to set this environment as your project interpreter."
    echo "(In PyCharm: Project Settings -> Project Interpreter -> gear Icon -> add -> existing environment (should default to this with correct settings.))"
    echo "Then run:"
    echo "    ./Scripts/reinitialize_database.sh"
    echo "    ./manage.py createsuperuser"
    echo "    ./Scripts/do_migration.sh"

fi