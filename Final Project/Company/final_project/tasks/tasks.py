from celery import shared_task, Celery

app = Celery('final_project', broker='amqp://127.0.0.1:5672',backend="django-db")
@shared_task(bind=True)
def calculate(self,cost, area, hours):
    result = cost * area * hours
    return result

@shared_task(bind=True)
def notify(self):
    print("New notification")
    return "Done"

