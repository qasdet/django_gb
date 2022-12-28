#!/bin/sh

python3 manage.py collectstatic --noinput
python3 manage.py flush --no-input
python3 manage.py makemigrations
python3 manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')" | python3 manage.py shell
echo "\n Superuser ${DJANGO_SUPERUSER_USERNAME} created\n"
python3 manage.py loaddata 001_news 002_courses 003_lessons 004_teachers

exec "$@"
