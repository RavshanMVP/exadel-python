from celery import shared_task, Celery
from django.core.mail import send_mail
from core.models import User, Notification, Request, RequestStatus
import os
os.environ.setdefault(value='final_project.settings.settings', key='DJANGO_SETTINGS_MODULE', )
app = Celery('final_project', broker='amqp://127.0.0.1:5672', backend="django-db")
import datetime
from django.utils import timezone
@shared_task(bind=True)
def calculate(self, cost, area, hours):
    result = cost * area * hours
    return result


@shared_task(bind=True)
def notify(self):
    one_off=True
    print("New notification")
    return "Done"


@shared_task(bind=True)
def send_notification(self, service_name, recipient, company_name, user_name, address, cost_total, category, email,
                      phone):
    send_mail(
        recipient_list=[recipient],
        subject=service_name,
        message=("Dear " + company_name + ",\n"
                                          "a user " + user_name + " ordered a request of " + category +
                 " with a total cost of " + str(cost_total) + ".\n"
                 + "the address of the user: " + address + ".\n"
                 + "Please, go to http://127.0.0.1:8000/responses/list/ to accept or cancel that request.\n"
                 + "You can contact them by " + email + " or " + phone + ".\n"),
        from_email="ravshan020703@gmail.com",
        fail_silently=False,
    )

    Note = Notification(subject=service_name, sender=company_name, recipient=recipient,
                        message=("Dear " + company_name + "\n"
                                 + "a user " + user_name + " ordered a request with a total cost of " +
                                 str(cost_total)))
    Note.save()

    return "Done"


@shared_task(bind=True)
def respond(self, verdict, company_name, service_name, user_name, email):
    Note = Notification(subject=service_name, sender=company_name, recipient=user_name,
                        message=("Dear " + str(user_name) + "\n"
                                 + "a company " + company_name + " accepted your offer.\n"))
    Note.save()
    send_mail(
        from_email="ravshan020703@gmail.com",
        subject=service_name,
        recipient_list=[email],
        message=("Dear " + str(user_name) + "\n"
                 + "a company " + company_name + " accepted your offer.\n"),
        fail_silently=False,
    )
    return "Sent"


@shared_task(bind=True)
def respond_negative(self, company_name, service_name, user_name, email):
    Note = Notification(subject=service_name, sender=company_name, recipient=user_name,
                        message=("Dear " + str(user_name) + "\n"
                                 + "a company " + company_name + " has denied your offer.\n"
                                 + "Sorry for the incovenience"))
    Note.save()
    send_mail(
        from_email="ravshan020703@gmail.com",
        subject=service_name,
        recipient_list=[email],
        message=("Dear " + str(user_name) + "\n"
                 + "a company " + company_name + " has denied your offer.\n"
                 + "Sorry for the incovenience"),
        fail_silently=False,
    )

    return "Sent"

@shared_task(bind=True)
def confirm(self, company_name, service_name, user_name, email):
    Note = Notification(subject=service_name, sender=user_name, recipient=company_name,
                        message=("Dear " + str(company_name) + "\n"
                                 + "a user " + user_name + " confirmed your offer.\n"
                                 + "You can start cleaning now :)"))
    Note.save()
    send_mail(
        from_email="ravshan020703@gmail.com",
        subject=service_name,
        recipient_list=[email],
        message=("Dear " + str(company_name) + "\n"
                 + "a user " + user_name + " confirmed your offer.\n"
                 + "You can start cleaning now :)"),
        fail_silently=False,
    )

    return "Sent"

@shared_task(bind=True)
def change_status(self, request):
    time_change = datetime.timedelta(minutes=int(request.minutes))
    new_time = request.created_at + time_change
    print(new_time)
    print(request.minutes)
    now = timezone.now()
    while now < new_time:
        now = timezone.now()
    request.status = RequestStatus.objects.get(status="Completed")
    request.save()
    return "Changed"
