# Python 이미지를 기반으로 합니다.
FROM python:3.12

# 환경변수를 설정합니다.
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리를 설정합니다.
WORKDIR /app

# 필요한 패키지를 설치합니다.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성을 설치합니다.
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# playwright 설치
RUN playwright install-deps
RUN playwright install

# 애플리케이션 코드를 복사합니다.
COPY . .

RUN chmod +x scripts/wait-for-it.sh

# Celery worker를 실행합니다.
CMD ["scripts/wait-for-it.sh", "rabbitmq:5672", "--", "celery", "-A", "run", "worker", "-Q", "webinars-beat,webinars", "--loglevel=info", "--logfile=./logs/celery_worker.log"]