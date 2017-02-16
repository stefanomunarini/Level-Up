from django.db.models import Sum
from django.db.models.functions import Coalesce

from games import services
from levelup import services as levelup_services
from transactions.models import Transaction


def get_sale_stats(developer):
    earnings = Transaction.objects.filter(game__in=developer.get_developed_games())\
        .aggregate(earnings=Coalesce(Sum('amount'), 0)).get('earnings')
    stats = {
        'developer': developer.display_name,
        'developer_slug': developer.url_slug,
        'earnings': earnings,
        'games_developed': [
            {
                'name': game.name,
                'earnings': services.get_game_stats(game).get('amount_earned'),
                'downloads': game.downloads,
                'played': game.plays
            }
            for game
            in developer.get_developed_games()
            if game.downloads > 0
        ]
    }
    return stats


def get_developed_games(api_token_obj):
    developed_games = api_token_obj.developer.get_developed_games()
    return _serialize_games(developed_games)


def get_game_stats(game):
    dev = game.dev
    stats = {
        'name': game.name,
        'slug': game.slug,
        'price': game.price,
        'category': game.category,
        'developer': {
            'name': dev.display_name,
            'url_slug': dev.url_slug,
            'website': dev.website
        },
        'downloads': game.downloads,
        'played': game.plays
    }
    return stats


def search_game(filtered_games):
    return _serialize_games(filtered_games)


def get_top_games():
    top_games = {}
    game_categories = levelup_services.get_homepage_games(10)
    for game_category_list in game_categories:
        games = game_categories[game_category_list]
        top_games[game_category_list] = _serialize_games(games)
    return top_games


def _serialize_games(games):
    serialized_games = []
    for game in games:
        serialized_games.append({
            'name': game.name,
            'slug': game.slug,
            'price': game.price,
            'downloads': game.downloads,
            'plays': game.plays,
            'description': game.description,
            'developer': game.dev.display_name,
            'category': game.category
        })
    return serialized_games
