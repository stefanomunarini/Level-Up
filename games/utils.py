from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _

from games.forms import GameScreenshotModelFormSet
from games.models import Game, GameScreenshot


class GameOwnershipRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            dispatcher = super(GameOwnershipRequiredMixin, self).dispatch(request, *args, **kwargs)
            self.object = self.get_object()
            if self.object not in request.user.profile.get_bought_games():
                messages.error(request,
                               _('Hey {}, you must buy the game before being able to play!'.format(request.user.profile)))
                return HttpResponseRedirect(reverse_lazy('game:detail', kwargs={'slug': self.object.slug}))
            return dispatcher
        messages.error(request, _('You must be authenticated to perform this action!'))
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


class GameCreateUpdateMixin(object):
    """
    This mixin provides shared functionality for creating and updating a game. In particular, it checks that the user
    is authenticated and has a 'Developer' profile.
    Moreover, provide functionality to save/update screenshot
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.profile.is_developer:
            raise PermissionDenied
        return super(GameCreateUpdateMixin, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        game = form.instance
        game.dev = self.request.user.profile
        game.save()
        game_screenshot_formset = GameScreenshotModelFormSet(self.request.POST,
                                                             self.request.FILES)
        game_screenshot_instances = game_screenshot_formset.save(commit=False)
        for game_screenshot_instance in game_screenshot_instances:
            game_screenshot_instance.game = game
            game_screenshot_instance.save()

        return super(GameCreateUpdateMixin, self).form_valid(form)

    def get_screenshot_formset(self, game_filter=None):
        formset = GameScreenshotModelFormSet()
        if game_filter:
            formset.queryset = GameScreenshot.objects.filter(game=game_filter)
        else:
            formset.queryset = GameScreenshot.objects.none()
        return formset
