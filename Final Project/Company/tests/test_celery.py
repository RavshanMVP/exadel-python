from final_project.tasks.tasks import calculate, notify, send_notification, respond, respond_negative, confirm
from final_project.tasks.celery import debug_task
from random import randint
import pytest

pytestmark = pytest.mark.django_db


# class TestCelery:
#     def test_notify(self, celery_worker):
#         result = notify.delay()
#
#         assert result.get() == "Done"
#         assert result.ready() is True
#
#     def test_calculate(self, celery_worker):
#         hours = randint(1, 3)
#         cost = randint(5, 50)
#         area = randint(40, 200)
#         result = calculate.delay(cost, area, hours)
#
#         assert result.get() == cost*area*hours
#         assert result.ready() is True
#
#     def test_debug(self, celery_worker):
#         result = debug_task.delay()
#         assert result.ready() is False
#
#     def test_notification(self, celery_worker):
#         result = send_notification.delay(email="1@gmail.com", recipient="2@gmail.com", category="", address="", phone="",
#                                          service_name="", company_name="", user_name="", cost_total="")
#         assert result.get() == "Done"
#
#     def test_respond(self,celery_worker):
#         result = respond.delay(verdict="!", company_name="1",service_name="1",user_name=1,email="1")
#         assert result.get() == "Sent"
#
#     def test_respond_negative(self,celery_worker):
#         result = respond_negative.delay(company_name="1",service_name="1",user_name=1,email="1")
#         assert result.get() == "Sent"
#
#     def test_respond_negative(self,celery_worker):
#         result = respond_negative.delay(company_name="1",service_name="1",user_name=1,email="1")
#         assert result.get() == "Sent"
