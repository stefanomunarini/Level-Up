from datetime import date, timedelta

from django.db.models import Count

from games.models import Game


def get_homepage_games(elements_to_show):
    games = Game.objects.all()
    today = date.today()
    return {
        'best_sellers': get_best_sellers(games)[:elements_to_show],
        'trending_this_week': get_trending_this_week(games, today)[:elements_to_show],
        'trending_this_month': get_trending_this_month(games, today)[:elements_to_show]
    }


def get_best_sellers(games):
    return games.annotate(downloads=Count('transactions')) \
        .order_by('-downloads') \
        .filter(downloads__gt=0)


def get_trending_this_week(games, today):
    one_week_ago = today - timedelta(7)
    return games.filter(transactions__datetime__gte=one_week_ago) \
        .annotate(downloads=Count('transactions')) \
        .order_by('-downloads')


def get_trending_this_month(games, today):
    one_month_ago = today - timedelta(31)
    return games.filter(transactions__datetime__gte=one_month_ago) \
        .annotate(downloads=Count('transactions')) \
        .order_by('-downloads')
