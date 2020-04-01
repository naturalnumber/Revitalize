#!/usr/bin/env bash

# creates 5 basic users with: username, email, password, firstname and lastname

set -o errexit
set -o pipefail

echo "Generating Test Users"

echo "
from Revitalize.models import User;
passTemp = User.objects.make_random_password(15)
print(passTemp);
user = User.objects.create_user('TesterOne', User.objects.normalize_email('one@tesTer.com'), passTemp);
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
user.save();
user = User.objects.create_superuser('labtech', '', 'cs4820');
user.is_lab_tech = True;
user.save();" | python $PWD/manage.py shell

echo "Created Test Users 1, 2, 3, 4, 5"
