from datetime import date, timedelta

from games.models import Game


def get_homepage_games(elements_to_show):
    games = Game.objects.all().prefetch_related('transactions', 'transactions__game', 'scores')
    today = date.today()
    return {
        'best_sellers': get_best_sellers(games)[:elements_to_show],
        'trending_this_week': get_trending_this_week(games, today)[:elements_to_show],
        'trending_this_month': get_trending_this_month(games, today)[:elements_to_show],
        'most_played': get_most_played(games)
    }


def get_best_sellers(games):
    return _order_and_filter(games, only_positive_downloads=True)


def get_trending_this_week(games, today):
    one_week_ago = today - timedelta(7)
    return _order_and_filter(games.filter(transactions__datetime__gte=one_week_ago), only_positive_downloads=True)


def get_trending_this_month(games, today):
    one_month_ago = today - timedelta(31)
    return _order_and_filter(games.filter(transactions__datetime__gte=one_month_ago), only_positive_downloads=True)


def get_most_played(queryset):
    return _order_and_filter(queryset, only_positive_downloads=True)


def _order_and_filter(queryset, order_by='-downloads', only_positive_downloads=False):
    queryset = queryset.order_by(order_by)
    if only_positive_downloads:
        return queryset.filter(downloads__gt=0)
    return queryset
