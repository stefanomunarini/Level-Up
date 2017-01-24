from django.db.models import Sum, Min
from django.db.models.functions import Coalesce

from transactions.models import Transaction


def get_game_stats(game):
    return Transaction.objects.filter(game=game, status=Transaction.SUCCESS_STATUS)\
        .aggregate(amount_earned=Coalesce(Sum('amount'), 0), first_sell=Min('datetime'))
