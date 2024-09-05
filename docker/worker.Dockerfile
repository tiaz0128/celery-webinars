FROM python:3.12

ENV PYTHONPATH=/worker:$PYTHONPATH
WORKDIR /worker

RUN pip install poetry

COPY pyproject.toml poetry.lock* /worker/
COPY .env /worker/
COPY run.py /worker/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY ./app/ /worker/app/
RUN mkdir -p /worker/logs /worker/.temp

CMD ["celery", "-A", "run", "worker", "-Q", "test-queue,beat-queue", "--hostname", "worker@%h", "-c", "4", "--loglevel=info"]