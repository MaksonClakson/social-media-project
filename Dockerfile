FROM python:3.9-slim

# `DJANGO_ENV` arg is used to make prod / dev builds:
ARG DJANGO_ENV \
  # Needed for fixing permissions of files created by Docker:
  UID=1000 \
  GID=1000

ENV DJANGO_ENV=${DJANGO_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.2.0 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

EXPOSE 8000

# System deps:
RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    curl \
  # Installing `poetry` package manager:
  && curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version

WORKDIR /code

# Add user, group and static, media folders
RUN groupadd -g "${GID}" -r web \
  && useradd -d '/code' -g web -l -r -u "${UID}" web \
  && chown web:web -R '/code' \
  # Static and media files:
  && mkdir -p '/var/www/django/static' '/var/www/django/media' \
  && chown web:web '/var/www/django/static' '/var/www/django/media'

# Copy only requirements to cache them in docker layer
COPY --chown=web:web poetry-project/poetry.lock poetry-project/pyproject.toml .env /code/

# Project initialization:
# RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
# Poetry will not create a new virtual environment
RUN poetry run pip install -U pip \
  && poetry config virtualenvs.create $POETRY_VIRTUALENVS_CREATE \
  && poetry install \
    $(if [ "$DJANGO_ENV" = 'production' ]; then echo '--no-dev'; fi) \
    --no-interaction --no-ansi --no-root

# Run this script as an entry point:
COPY ./scripts/entrypoint.sh /docker-entrypoint.sh

RUN chmod +x '/docker-entrypoint.sh'

# Running as non-root user:
USER web

ENTRYPOINT [ "/docker-entrypoint.sh" ]

# Creating folders, and files for a project:
COPY --chown=web:web ./core /code