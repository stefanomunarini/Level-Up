from __future__ import unicode_literals

from django.db import models

from users.models import UserProfile
from games.models import Game


class Transaction(models.Model):

    SUCCESS_STATUS = 'success'
    CANCEL_STATUS = 'cancel'
    ERROR_STATUS = 'error'
    PAYMENT_STATUSES_CHOICES = ((SUCCESS_STATUS, 'Success'),
                                (CANCEL_STATUS, 'Cancel'),
                                (ERROR_STATUS, 'Error'),)

    user = models.ForeignKey(UserProfile, related_name='transactions', on_delete=models.SET_NULL)
    game = models.ForeignKey(Game, related_name='transactions', on_delete=models.SET_NULL)
    datetime = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(null=False, blank=False, default=0.0)
    status = models.CharField(choices=PAYMENT_STATUSES_CHOICES)
