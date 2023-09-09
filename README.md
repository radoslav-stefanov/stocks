virtualenv -p `which python3.11` core

pip3 install django

django-admin startproject core

python3 manage.py migrate
