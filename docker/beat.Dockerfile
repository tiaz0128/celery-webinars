FROM python:3.12

ENV PYTHONPATH=/beat:$PYTHONPATH

WORKDIR /beat
RUN pip install poetry

COPY pyproject.toml poetry.lock* /beat/
COPY .env /beat/
COPY run.py /beat/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY ./app/ /beat/app/
RUN mkdir -p /beat/logs /beat/.temp

CMD ["celery", "-A", "run", "beat", "--loglevel=info"]