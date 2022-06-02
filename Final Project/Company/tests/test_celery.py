from final_project.tasks.tasks import calculate, notify
from final_project.tasks.celery import debug_task
from random import randint
import pytest

pytestmark = pytest.mark.django_db

class TestCelery:
    def test_notify(self, celery_worker):
        result = notify.delay()

        assert result.get() == "Done"
        assert result.ready() == True

    def test_calculate(self, celery_worker):
        hours = randint(1, 3)
        cost = randint(5, 50)
        area = randint(40, 200)
        result = calculate.delay(cost,area,hours)

        assert result.get() == cost*area*hours
        assert result.ready() == True

    def test_debug(self, celery_worker):
        result = debug_task.delay()
        result.get()
        assert result.ready() == True
