from celery import Celery

app = Celery("myproject", include=["app.tasks.add"])
app.config_from_object("app.celeryconfig")

if __name__ == "__main__":
    app.start()
