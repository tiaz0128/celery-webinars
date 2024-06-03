# Webinar 자동 시청 프로젝트

## 개발 동기

이 프로젝트는 새벽에(=AM 02:00 🤣) 하는 해외 웹비나를 도저히 참여 할 수 없어 만들었습니다.

<br/>

## 프로젝트 개요

정해진 시간에 특정 웹비나(isc2)를 자동으로 시청하게 해주는 애플리케이션 입니다. 구글 캘린더에 등록한 웹비나를 매일 확인하여 일정에 맞게 해당 웹비나에 자동으로 참석 합니다.

구현에 사용한 주요 라이브러리는 아래와 같습니다.

- Celery
- Google Calender API
- RabbitMQ
- Playwright

<br/>

## 설치

- Python 3.12
- playwright 설치 필요
- 의존성 관리는 Poetry를 사용
- Celery Beat & Worker daemon 등록

```sh
sudo playwright install-deps

playwright install
```

```sh
poetry install

celery -A run beat --loglevel=info --logfile=./logs/celery_beat.log

celery -A run worker -Q webinars --loglevel=info --logfile=./logs/celery_worker.log
```

### /etc/systemd/system/celery_beat.service

```sh
[Unit]
Description=Celery Beat
After=network.target
Requires=celery_worker.service

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/rabbit-celery
ExecStart=/home/ubuntu/rabbit-celery/.venv/bin/celery -A run beat --loglevel=info --logfile=./logs/celery_beat.log
Restart=always

[Install]
WantedBy=multi-user.target
```

### /etc/systemd/system/celery_worker.service

```sh
[Unit]
Description=Celery Worker
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/rabbit-celery
ExecStart=/home/ubuntu/rabbit-celery/.venv/bin/celery -A run worker -Q webinars --loglevel=info --logfile=./logs/celery_worker.log
Restart=always

[Install]
WantedBy=multi-user.target
```

```sh
sudo systemctl daemon-reload

sudo systemctl start celery_beat.service
sudo systemctl start celery_worker.service
```

<br/>

## 세부 동작

![architecture](asset/img/architecture.png)

### Publisher : Celery Beat

- Celery Beat: 스케줄러. 매일 00:00 시 정각에 특정 동작을 수행
- Google calendar API : Google Calendar 에서 등록되어 있는 일정 중에서 특정 webinar 정보를 가져옴

### Broker : RabbitMQ

- RabbitMQ: 브로커로 사용

### Worker : Celery

- Celery Worker: 비동기 작업 큐를 처리
- playwright : chromium 을 통해 webinar 시청
