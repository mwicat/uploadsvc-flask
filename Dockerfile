FROM python:3.11-alpine as base

RUN python3 -m pip install poetry

FROM base as build

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root

FROM build as app

WORKDIR /app

COPY ./src ./src
COPY run_app.sh ./

EXPOSE 5000

CMD ["/bin/sh", "run_app.sh"]
