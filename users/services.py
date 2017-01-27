from django.core.mail import send_mail
from django.template.loader import render_to_string

from levelup.settings import EMAIL_HOST_USER


def send_email(subject, template, recipients, context=None):
    body = render_to_string(template, context)
    send_mail(subject, body, EMAIL_HOST_USER, recipients, html_message=body)
