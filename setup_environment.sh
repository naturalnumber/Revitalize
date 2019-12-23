#!/usr/bin/env bash
ECHO "Welcome to the Revitalize Virtual Environment Setup"
ECHO "Your operating system has been determined to be: acceptable :)"
READ -p "Would you like to continue? Y/n" -n 1 -r
ECHO

if [[ $REPLY =~ ^[Yy]$ ]]
then
    python3.7 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi