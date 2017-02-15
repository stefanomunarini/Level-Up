from django.contrib import messages
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from games.models import Game


class GameOwnershipRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            dispatcher = super(GameOwnershipRequiredMixin, self).dispatch(request, *args, **kwargs)
            self.object = self.get_object()
            if self.object not in request.user.profile.get_bought_games():
                messages.error(request,
                               'Hey {}, you must buy the game before being able to play!'.format(request.user.profile))
                return HttpResponseRedirect(reverse_lazy('game:buy', kwargs={'slug': self.object.slug}))
            return dispatcher
        messages.error(request, 'You must be authenticated to perform this action!')
        return HttpResponseRedirect(
                reverse_lazy('game:detail', kwargs={'slug': self.kwargs.get(self.slug_url_kwarg)}))


class GameSearchMixin(object):

    def get_queryset(self):
        queryset = Game.objects.all()

        if hasattr(self, 'show_games_that_are'):
            if self.show_games_that_are == 'bought-by-the-user':
                queryset = self.request.user.profile.get_bought_games()
            elif self.show_games_that_are == 'developed-by-the-user':
                queryset = self.request.user.profile.get_developed_games()

        search = self.request.GET.get('q')
        category = self.request.GET.get('category')

        vector = SearchVector('name', 'description')
        query = None

        if search:
            for word in search.split():
                if not query:
                    query = SearchQuery(word)
                else:
                    query = query | SearchQuery(word)
            queryset = queryset.annotate(rank=SearchRank(vector, query)).order_by('-rank').filter(rank__gt=0)

        if category:
            queryset = queryset.filter(category=category)

        if not search:
            queryset = queryset.order_by('-date_added')

        return queryset.filter(is_published=True)
