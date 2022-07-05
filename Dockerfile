FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR  /app/
COPY Pipfile* /app/

RUN apt-get update
RUN pip install pipenv \
    && pipenv install --deploy --system --ignore-pipfile


COPY entrypoint.sh /app/
COPY arc-entrypoint.sh /app/
ENTRYPOINT /app/entrypoint.sh
ENTRYPOINT /app/arc-entrypoint.sh

COPY app /app/