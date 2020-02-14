#!/usr/bin/env bash

# creates 5 basic users with: username, email, password, firstname and lastname

set -o errexit
set -o pipefail

echo "Generating Test Users"

echo "
from django.contrib.auth.models import User;
user = User.objects.create_user('TesterOne', 'one@tester.com','test1234');
user.first_name = 'One';
user.last_name = 'One';
user.save();
user = User.objects.create_user('TesterTwo', 'two@tester.com','test1234');
user.first_name = 'Two';
user.last_name = 'Two';
user.save();
user = User.objects.create_user('TesterThree', 'three@tester.com','test1234');
user.first_name = 'Three';
user.last_name = 'Three';
user.save();
user = User.objects.create_user('TesterFour', 'four@tester.com','test1234');
user.first_name = 'Four';
user.last_name = 'Four';
user.save();
user = User.objects.create_user('TesterFive', 'five@tester.com','test1234');
user.first_name = 'Five';
user.last_name = 'Five';
user.save();" | python $PWD/manage.py shell

echo "Created Test Users 1, 2, 3, 4, 5"