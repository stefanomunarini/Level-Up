from django.db.models import Count

from games.models import Game


def get_best_sellers():
    return Game.objects.all()\
        .annotate(downloads=Count('transactions'))\
        .order_by('-downloads')
