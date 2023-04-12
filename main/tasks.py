from celery import shared_task


@shared_task
def send_email(x, y):
    return x + y
