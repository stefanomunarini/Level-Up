from datetime import date, timedelta

from games.models import Game


def get_homepage_games(elements_to_show):
    games = _order_and_filter(Game.objects.all(), only_positive_downloads=True).order_by('-plays')
    today = date.today()
    return {
        'best_sellers': get_best_sellers(games)[:elements_to_show],
        'trending_this_week': get_trending_this_week(games, today)[:elements_to_show],
        'trending_this_month': get_trending_this_month(games, today)[:elements_to_show],
        'most_played': get_most_played(games).order_by('-downloads')[:elements_to_show]
    }


def get_best_sellers(games):
    return games


def get_trending_this_week(games, today):
    one_week_ago = today - timedelta(7)
    return games.filter(transactions__datetime__gte=one_week_ago)


def get_trending_this_month(games, today):
    one_month_ago = today - timedelta(31)
    return games.filter(transactions__datetime__gte=one_month_ago)


def get_most_played(queryset):
    return _order_and_filter(queryset, order_by='-plays', only_positive_downloads=True)


def _order_and_filter(queryset, order_by='-downloads', only_positive_downloads=False):
    queryset = queryset.order_by(order_by)
    if only_positive_downloads:
        return queryset.filter(downloads__gt=0)
    return queryset
