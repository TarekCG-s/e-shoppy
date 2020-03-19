from celery import task
from django.core.mail import send_mail


@task
def send_email(subject, message, emails):
    return send_mail(subject, message, 'admin@eshoppy.com', emails)
