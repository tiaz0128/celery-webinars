# Webinar 자동 시청 프로젝트

## 개발 동기

이 프로젝트는 새벽에(=보통 02:00) 하는 해외 웹비나를 참석을 도저히 할 수가 없어 만들었습니다.

## 프로젝트 개요

정해진 시간에 특정 웹비나(isc2)를 자동으로 시청하게 해주는 애플리케이션 입니다. 구글 캘린더에 등록한 웹비나를 매일 확인하여 일정에 맞게 해당 웹비나에 자동으로 참석 합니다.

구현에 사용한 주요 라이브러리는 아래와 같습니다.

- Celery beat
- Celery worker
- Google calender API
- RabbitMQ
- Playwright

## 설치

- Python 3.12
- 의존성 관리는 Poetry를 사용합니다.
- 개발 환경은 WSL2 (ubuntu 22.04) 에서 개발

```sh
# 프로젝트 의존성 설치
poetry install

celery -A run beat --loglevel=info --logfile=./logs/celery_beat.log

celery -A run worker -Q work-page --loglevel=info --logfile=./logs/celery_worker.log
```

## 세부 동작

![architecture](asset/img/architecture.png)

### Publisher

- Celery beat: 스케줄러. 매일 00:00 시 정각에 특정 동작을 수행
- Google calendar API : Google Calendar 에서 등록되어 있는 일정 중에서 특정 webinar 정보를 가져옴

### Broker

- RabbitMQ: 브로커로 사용

### Worker

- Celery: 비동기 작업 큐를 처리
- playwright : chromium 을 통해 webinar 시청
