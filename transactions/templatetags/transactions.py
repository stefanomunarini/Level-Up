from __future__ import absolute_import

from _md5 import md5

from django import template
from django.urls import reverse

from levelup.settings import PAYMENT_SERVICE_SELLER_ID, PAYMENT_SERVICE_SECRET_KEY
from transactions.forms import TransactionForm

register = template.Library()


@register.simple_tag(takes_context=True)
def transaction_form(context, game):
    pid = game.slug
    sid = PAYMENT_SERVICE_SELLER_ID
    amount = game.price

    secret_key = PAYMENT_SERVICE_SECRET_KEY
    checksum_str = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    checksum = md5(checksum_str.encode("ascii")).hexdigest()

    # dynamically build the url so it works for both dev and prod
    webapp_url = context.request.is_secure() and 'https://' or 'http://'
    webapp_url += context.request.META['HTTP_HOST']

    redirect_url = webapp_url + reverse('transactions:result')

    data = {
        "pid": pid,
        "sid": sid,
        "amount": amount,
        "checksum": checksum,
        "success_url": redirect_url,
        "cancel_url": redirect_url,
        "error_url": redirect_url,
    }

    return TransactionForm(data)
