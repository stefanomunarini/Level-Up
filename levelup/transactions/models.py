from __future__ import unicode_literals

from django.db import models

from games.models import Game


class Transaction(models.Model):

    SUCCESS_STATUS = 'success'
    CANCEL_STATUS = 'cancel'
    ERROR_STATUS = 'error'
    PAYMENT_STATUSES_CHOICES = ((SUCCESS_STATUS, 'Success'),
                                (CANCEL_STATUS, 'Cancel'),
                                (ERROR_STATUS, 'Error'),)

    user = models.ForeignKey('users.UserProfile', related_name='transactions')
    game = models.ForeignKey(Game, related_name='transactions')
    datetime = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(null=False, blank=False, default=0.0)
    status = models.CharField(max_length=16, choices=PAYMENT_STATUSES_CHOICES)
