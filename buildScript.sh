#!/bin/sh
# O shell irá encerrar a execução do script quando um comando falhar
set -e

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py shell -c "from django.contrib.auth.models import User; \
                           User.objects.filter(username='admin').exists() or \
                           User.objects.create_superuser('admin','admin@gmai.com', 'admin123')"

#python manage.py runserver 0.0.0.0:8000
gunicorn --bind 0.0.0.0:8000 --access-logfile - phoneCalls.wsgi:application