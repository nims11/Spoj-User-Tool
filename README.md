# Spoj User Tool
Django based Spoj User Analysis tool.
Currently hosted on Google Appengine: http://spojtool.appspot.com/

## Installation
Get the packages listed on http://www.allbuttonspressed.com/projects/djangoappengine and place them inside the project directory as specified.

Create a file secret_key.py in the root directory and add a line
***
SECRET_KEY = 'Your_secret_key'
***

The standard manage.py commands will work.

Use
./manage.py deploy to deploy it to appengine.

Make sure to set DEBUG to false in settings.py before deploying.