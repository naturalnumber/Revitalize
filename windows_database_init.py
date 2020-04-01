
# To load this run:
# python ./manage.py shell
# (or use the 'Django Shell' start configuration)
# Then enter:
# exec(open("./windows_database_init.py").read())
# if you don't want to auto load the surveys and profiles, set the below variable to False first
# if it is True, you don't need to run the other scripts

load_all = True

from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', '', 'cs4820')

if load_all:
    exec(open("./load_profiles.py").read())
    exec(open("./load_surveys.py").read())
