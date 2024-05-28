import logging
import pytest

from app.tasks.add import add


class TestCelery:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_celery_add_task(self):
        add.delay(4, 4)
