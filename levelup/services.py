from datetime import date, timedelta

from games.models import Game


def get_homepage_games(elements_to_show):
    games = _order_and_filter(Game.objects.filter(is_published=True), only_positive_downloads=True)
    today = date.today()
    return {
        'best_sellers': get_best_sellers(games)[:elements_to_show],
        'trending_this_week': get_trending_this_week(games, today)[:elements_to_show],
        'trending_this_month': get_trending_this_month(games, today)[:elements_to_show],
        'most_played': get_most_played()[:elements_to_show]
    }


def get_best_sellers(games):
    return games


def get_trending_this_week(games, today):
    one_week_ago = today - timedelta(7)
    return games.filter(transactions__datetime__gte=one_week_ago)


def get_trending_this_month(games, today):
    one_month_ago = today - timedelta(31)
    return games.filter(transactions__datetime__gte=one_month_ago)


def _order_and_filter(queryset, only_positive_downloads=False):
    queryset = queryset.order_by('-downloads', '-plays')
    if only_positive_downloads:
        return queryset
    return queryset


def get_most_played():
    return Game.objects.all().order_by('-plays', '-downloads').filter(downloads__gt=0, is_published=True)
