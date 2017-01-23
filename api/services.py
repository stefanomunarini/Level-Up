from django.db.models import Sum
from django.db.models.functions import Coalesce

from transactions.models import Transaction


def get_developed_games(api_token_obj):
    developed_games = api_token_obj.developer.get_developed_games()
    serialized_games = []
    for game in developed_games:
        serialized_games.append({
            'name': game.name,
            'slug': game.slug,
            'price': game.price,
            'downloads': game.downloads,
            'plays': game.plays
        })
    return serialized_games


def get_sale_stats(api_token_obj):
    return Transaction.objects.filter(game__in=api_token_obj.developer.get_developed_games())\
        .aggregate(earnings=Coalesce(Sum('amount'), 0))
