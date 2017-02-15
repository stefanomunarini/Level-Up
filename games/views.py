from _md5 import md5

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from games import services
from games.forms import GameScreenshotModelFormSet, GameUpdateModelForm, GameSearchForm
from games.models import Game, GameState, GameScore, GameScreenshot
from games.utils import GameOwnershipRequiredMixin, GameSearchMixin
from levelup.settings import PAYMENT_SERVICE_SELLER_ID, PAYMENT_SERVICE_SECRET_KEY
from transactions.forms import TransactionForm
from transactions.models import Transaction
from transactions.views import save_transaction


class GameListView(GameSearchMixin, FormMixin, ListView):
    """
    A view that is used whenever a list of games needs to be shown
    Games to be displayed are controlled by passing attribute values in the url dispatcher
    """
    context_object_name = 'games'
    form_class = GameSearchForm
    template_name = 'game_list.html'
    page_title = _('Games')
    paginate_by = 30
    paginate_orphans = 3
    # an attribute that can be used in the url dispatcher to customize the view
    show_games_that_are = ''

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def get_initial(self):
        initial = super(GameListView, self).get_initial()
        initial['q'] = self.request.GET.get('q')
        initial['category'] = self.request.GET.get('category')
        return initial


class GameDetailView(DetailView):
    model = Game
    context_object_name = 'game'
    results_to_show = 10
    template_name = 'game_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = self.request.user.profile
            if user_profile.is_developer and user_profile == self.get_object().dev:
                context['game_stats'] = services.get_game_stats(self.get_object())
            context['global_scores'] = services.get_game_global_scores(self.object,
                                                                       results_to_show=self.results_to_show)
        return context


class GamePlayView(GameOwnershipRequiredMixin, GameDetailView):
    results_to_show = 10
    template_name = 'game_play.html'

    def get_context_data(self, **kwargs):
        context = super(GamePlayView, self).get_context_data(**kwargs)
        context['game_state'] = GameState.objects.filter(game=self.object,
                                                         user=self.request.user.profile).last()
        context['my_scores'] = GameScore.objects.filter(game=self.object,
                                                        player=self.request.user.profile)\
                                        .order_by('-score', '-timestamp')[:self.results_to_show]
        context['global_scores'] = services.get_game_global_scores(self.object, results_to_show=self.results_to_show)
        return context


class GameStateView(GameOwnershipRequiredMixin, SingleObjectMixin, View):
    model = Game

    def dispatch(self, request, *args, **kwargs):
        dispatcher = super(GameStateView, self).dispatch(request, *args, **kwargs)
        if isinstance(dispatcher, HttpResponseRedirect):
            return dispatcher

        game_state = GameState()
        game_state.user = request.user.profile
        game_state.game = self.get_object()
        game_state.state = request.POST.get('game_state')
        game_state.save()

        dispatcher.status_code = 200
        return dispatcher


class GameScoreView(GameOwnershipRequiredMixin, SingleObjectMixin, View):
    model = Game

    def dispatch(self, request, *args, **kwargs):
        dispatcher = super(GameScoreView, self).dispatch(request, *args, **kwargs)
        if isinstance(dispatcher, HttpResponseRedirect):
            return dispatcher

        game = self.get_object()
        user = request.user.profile

        game_score = GameScore()
        game_score.player = user
        game_score.game = game
        game_score.score = request.POST.get('game_score')
        game_score.save()

        GameState.objects.filter(game=game, user=user).delete()

        dispatcher.status_code = 200
        return dispatcher


class NewGameView(GameOwnershipRequiredMixin, SingleObjectMixin, View):
    """
    This view simply reset the GameState in order to start a new game. Its only function is to remove the previous
    saved GameState for a particular Game and UserProfile.
    """
    http_method_names = ('GET',)
    model = Game

    def dispatch(self, request, *args, **kwargs):
        dispatcher = super(NewGameView, self).dispatch(request, *args, **kwargs)
        if isinstance(dispatcher, HttpResponseRedirect):
            return dispatcher
        GameState.objects.filter(game=self.get_object(), user=request.user.profile).delete()
        dispatcher.status_code = 200
        return dispatcher


"""
DEVELOPERS VIEWS
"""


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


class GameCreateView(GameCreateUpdateMixin, CreateView):
    fields = ('name', 'slug', 'url', 'icon', 'description', 'price', 'category')
    model = Game
    template_name = 'game_create.html'
    success_url = reverse_lazy('profile:user-profile')

    def get_context_data(self, **kwargs):
        context = super(GameCreateView, self).get_context_data(**kwargs)
        context['game_screenshot_forms'] = self.get_screenshot_formset()
        return context


class GameUpdateView(GameCreateUpdateMixin, UpdateView):
    model = Game
    context_object_name = 'game'
    form_class = GameUpdateModelForm
    template_name = 'game_update.html'

    def get_context_data(self, **kwargs):
        context = super(GameUpdateView, self).get_context_data(**kwargs)
        context['game_screenshot_forms'] = self.get_screenshot_formset(self.get_object())
        return context

    def get_object(self, queryset=None):
        self.object = super(GameUpdateView, self).get_object(queryset)
        if self.object not in self.request.user.profile.get_developed_games():
            raise PermissionDenied
        return self.object

    def get_success_url(self):
        return reverse_lazy('game:detail', kwargs={'slug': self.object.slug})


class GameDeleteView(LoginRequiredMixin, DeleteView):
    model = Game

    def get_success_url(self):
        return reverse_lazy('game:detail', kwargs={'slug': self.object.slug})

    def get_object(self, queryset=None):
        obj = super(GameDeleteView, self).get_object(queryset=queryset)
        if not obj.dev == self.request.user.profile:
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        self.object.is_published = not self.object.is_published
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TicTacToe(TemplateView):
    template_name = 'tictactoe.html'

    @xframe_options_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(TicTacToe, self).dispatch(request, *args, **kwargs)
