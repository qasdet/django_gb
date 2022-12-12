FROM python:3.10.5-slim-bullseye

RUN mkdir /init
WORKDIR /init

RUN apt-get update && apt-get upgrade -y \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

ENV DJANGO_SETTINGS_MODULE=config.settings \
  # python
  PYTHONPATH=${PYTHONPATH}:${PWD} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_ROOT_USER_ACTION=ignore \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.1.13 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' 

ADD pyproject.toml .

RUN python3 -m pip install --upgrade pip && \
  pip3 install poetry && \
  poetry config virtualenvs.create false && \
  poetry install --no-dev && \
  rm -rf ${POETRY_CACHE_DIR}

VOLUME ["/app"]
WORKDIR /app

RUN chown -R app:app /app
USER app
