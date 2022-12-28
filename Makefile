#!make

WORK_DIR=$(shell pwd)
DOCKER_USER=$(shell whoami)


djkey:
	python -c "from django.core.management.utils import get_random_secret_key;print(get_random_secret_key())"


prepare-folders:
	mkdir -p ./data/cache
	mkdir -p ./data/rabbitmq/data
	mkdir -p ./data/rabbitmq/log


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


trans:
	./manage.py mm
	./manage.py cm



down: containers-down purge-data

down-force: fix-docker-permission-denied down

reset: down up

start: runserver
