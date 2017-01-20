from datetime import date, timedelta

from django.db.models import Case
from django.db.models import Count, IntegerField
from django.db.models import When

from games.models import Game
from transactions.models import Transaction


def get_homepage_games(elements_to_show):
    games = Game.objects.all()
    today = date.today()
    return {
        'best_sellers': get_best_sellers(games)[:elements_to_show],
        'trending_this_week': get_trending_this_week(games, today)[:elements_to_show],
        'trending_this_month': get_trending_this_month(games, today)[:elements_to_show]
    }


def get_best_sellers(games):
    return _annotate_downloads(games)


def get_trending_this_week(games, today):
    one_week_ago = today - timedelta(7)
    return _annotate_downloads(games.filter(transactions__datetime__gte=one_week_ago))


def get_trending_this_month(games, today):
    one_month_ago = today - timedelta(31)
    return _annotate_downloads(games.filter(transactions__datetime__gte=one_month_ago))


def _annotate_downloads(queryset):
    return queryset.annotate(downloads=Count(Case(
        When(transactions__status=Transaction.SUCCESS_STATUS, then=1),
        output_field=IntegerField(),
    ))).order_by('-downloads').filter(downloads__gt=0)
