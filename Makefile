#!make
include config/.env
export

GREEN=\033[4;92m
RED=\033[0;31m
NC=\033[0m
WORK_DIR=$(shell pwd)
DOCKER_USER=$(shell whoami)


djkey:
	python -c "from django.core.management.utils import get_random_secret_key;print(get_random_secret_key())"

install:
	sudo apt install python3-pip python3-poetry python3-cachecontrol docker.io docker-compose gettext -y 
	sudo usermod -aG docker ${DOCKER_USER}
	sudo systemctl enable docker
	sudo systemctl restart docker
	sudo docker pull redis
	sudo docker pull celery
	sudo docker pull rabbitmq:3-management
	poetry install

reset-db:
	rm -f ./data/database/db.sqlite3
	python manage.py migrate
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser($(DJANGO_SUPERUSER_USERNAME), $(DJANGO_SUPERUSER_EMAIL), $(DJANGO_SUPERUSER_PASSWORD))" | python manage.py shell
	echo "\n ${GREEN}Superuser ${DJANGO_SUPERUSER_USERNAME} created${NC}\n"
	python manage.py loaddata 001_news 002_courses 003_lessons 004_teachers

prepare-folders:
	mkdir -p ./data/cache
	mkdir -p ./data/rabbitmq/data
	mkdir -p ./data/rabbitmq/log
	# chown -R lxd:user ./data/cache
	# chown -R lxd:user ./data/rabbitmq
	# chmod -R 775 ./data/cache
	# chmod -R 775 ./data/rabbitmq

purge-data:
	rm -rf ./var/log/*
	rm -rf ./var/email-messages/*
	sudo rm -rf ./data/cache/*
	sudo rm -rf ./data/rabbitmq/log/*
	sudo rm -rf ./data/rabbitmq/data/*
	sudo rm -rf ./data/rabbitmq/data/.erlang.cookie
	

containers-up:
#	docker run -d --hostname redis --name redis -p 6379:6379 -v ${WORK_DIR}/data/cache:/data redis redis-server --save 20 1 --loglevel warning
#	docker run -d --hostname rabbitmq --name rabbitmq -e RABBITMQ_DEFAULT_USER=${RABBITMQ_DEFAULT_USER} -e RABBITMQ_DEFAULT_PASS=${RABBITMQ_DEFAULT_PASS} -p 5672:5672 -p 15672:15672 -v ${WORK_DIR}/data/rabbitmq/data:/var/lib/rabbitmq -v ${WORK_DIR}/data/rabbitmq/log:/var/log/rabbitmq rabbitmq:3-management	
	docker-compose -f stack.yml up -d

containers-up-verbose:
	docker-compose -f stack.yml up

containers-down:
#	docker rm -fv redis
#	docker rm -fv rabbitmq
	docker-compose -f stack.yml down

fix-docker-permission-denied:
	sudo aa-remove-unknown

runserver:
	./manage.py runserver 0.0.0.0:8000 --insecure

celery:
	celery -A config worker -l info

trans:
	./manage.py mm
	./manage.py cm

up: trans prepare-folders purge-data reset-db containers-up celery

down: containers-down purge-data

down-force: fix-docker-permission-denied down

reset: down up

start: runserver
