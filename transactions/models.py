from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Transaction(models.Model):

    SUCCESS_STATUS = 'success'
    CANCEL_STATUS = 'cancel'
    ERROR_STATUS = 'error'
    PAYMENT_STATUSES_CHOICES = ((SUCCESS_STATUS, _('Success')),
                                (CANCEL_STATUS, _('Cancel')),
                                (ERROR_STATUS, _('Error')),)

    user = models.ForeignKey('users.UserProfile', related_name='transactions')
    game = models.ForeignKey('games.Game', related_name='transactions')
    datetime = models.DateTimeField(default=timezone.now)
    amount = models.FloatField(null=False, blank=False, default=0.0)
    status = models.CharField(max_length=16, choices=PAYMENT_STATUSES_CHOICES)

    # a reference to the payment returned by the payment service provider
    payment_ref = models.IntegerField(null=True, blank=True)
