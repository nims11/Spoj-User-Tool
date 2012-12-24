# Spoj User Tool
Django based Spoj User Analysis tool.
Currently hosted on Google Appengine: http://spojtool.appspot.com/

## Installation
Get the packages listed on http://www.allbuttonspressed.com/projects/djangoappengine and place them inside the project directory as specified.

For Safety modify the SECRET_KEY in secret_key.py

The standard manage.py commands will work.

Use
./manage.py deploy to deploy it to appengine.
./manage.py runserver to test on local machine.

Make sure to set DEBUG to false in settings.py before deploying.
