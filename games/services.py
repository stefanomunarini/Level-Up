from django.db.models import Sum, Min
from django.db.models.functions import Coalesce

from games.models import GameScore
from transactions.models import Transaction


def get_game_stats(game):
    return Transaction.objects.filter(game=game, status=Transaction.SUCCESS_STATUS)\
        .aggregate(amount_earned=Coalesce(Sum('amount'), 0), first_sell=Min('datetime'))


def get_game_global_scores(game, results_to_show=10):
    return GameScore.objects.filter(game=game) \
        .order_by('-score', '-start_time')[:results_to_show]
