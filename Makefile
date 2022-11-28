#!make
include ./.env
export

WORK_DIR=$(shell pwd)
DOCKER_USER=$(shell whoami)


djkey:
	python -c "from django.core.management.utils import get_random_secret_key;print(get_random_secret_key())"

install:
	sudo apt update && sudo apt upgrade -y
	sudo apt install python-is-python3
	sudo apt install python3-pip python3-poetry python3-cachecontrol docker.io docker-compose gettext -y 
	sudo usermod -aG docker ${DOCKER_USER}
	sudo systemctl enable docker && sudo systemctl restart docker
	sudo docker pull postgres
	sudo docker pull adminer
	sudo docker pull redis
	sudo docker pull nginx
	sudo docker pull rabbitmq:3-management
	poetry install --no-dev

reset-db:
	sudo rm -rf ./data/database/pg_data/*
	rm -f ./data/database/db.sqlite3

prepare-folders:
	mkdir -p ./data/cache
	mkdir -p ./data/rabbitmq/data
	mkdir -p ./data/rabbitmq/log
	sudo chown -R django:lxd ./var
	sudo chown -R django:lxd ./data

purge-data:
	rm -rf ./var/log/*
	rm -rf ./var/email-messages/*
	sudo rm -rf ./static/admin
	sudo rm -rf ./static/debug_toolbar
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
	./manage.py runserver 0.0.0.0:8000 --insecuree

ip:
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' nginx
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' celery
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' rabbitmq
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' adminer

trans:
	./manage.py mm
	./manage.py cm

up: trans prepare-folders purge-data reset-db containers-up

down: containers-down purge-data

down-force: fix-docker-permission-denied down

reset: down up

reset-build: down up-build

start: runserver
