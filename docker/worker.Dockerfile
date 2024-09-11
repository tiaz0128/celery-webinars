FROM python:3.12

ENV PYTHONPATH=/worker:$PYTHONPATH
WORKDIR /worker

RUN pip install poetry

COPY pyproject.toml poetry.lock* /worker/
COPY run.py /worker/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY ./.temp/ /worker/.temp/
COPY ./app/ /worker/app/
RUN mkdir -p /worker/logs /worker/.temp

RUN playwright install
RUN playwright install-deps

CMD ["celery", "-A", "run", "worker", "-Q", "webinars-beat,webinars", "--hostname", "worker@%h", "-c", "4", "--loglevel=info"]