ARG DB_PATH
ARG MONGO_PATH
FROM python:3.9-slim-buster

ARG DB_PATH
ENV DB_PATH=${DB_PATH}

ARG MONGO_PATH
ENV MONGO_PATH=${MONGO_PATH}

RUN set -ex \
    && apt-get update -y \
    && apt-get install -y libpq-dev build-essential postgresql-client sqlite3 \
    && mkdir /code \
    && groupadd -g 999 appuser \
    && useradd -r -d /code -u 999 -g appuser appuser

WORKDIR /code

COPY . /code

COPY $DB_PATH /code
COPY $MONGO_PATH /code

COPY requirements.txt ./requirements.txt

RUN pip install -U pip \
    && pip install -r requirements.txt \
    && pip install . \
    && chown -R appuser:appuser -R /code

USER appuser

ENTRYPOINT ["bash", "/code/docker-entrypoint.sh" ]
