FROM python:3.9-slim

ENV POETRY_VERSION=1.2.0 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME='/usr/local'


# System deps:
RUN \
    apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    curl \
    # Installing 'poetry' package manager:
    && curl -sSL 'https://install.python-poetry.org' | python -

WORKDIR /app

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml /app/

# Initialization of poetry env:
RUN poetry run pip install -U pip \
    && poetry config virtualenvs.create $POETRY_VIRTUALENVS_CREATE \
    && poetry install --no-interaction --no-ansi --no-root

EXPOSE 8001

COPY ./scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x '/entrypoint.sh'
ENTRYPOINT [ "/entrypoint.sh" ]

COPY . /app/

