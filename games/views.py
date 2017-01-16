from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Min
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView

from games.forms import GameBuyForm, GameScreenshotModelFormSet
from games.models import Game
from transactions.models import Transaction


class GameListView(LoginRequiredMixin, ListView):
    """
    A view that is used whenever a list of games needs to be shown
    Games to be displayed are controlled by passing attribute values in the url dispatcher
    """
    login_url = reverse_lazy('login')
    context_object_name = 'games'
    template_name = 'game_list.html'
    bought = False  # Display only games that the user has bought
    page_title = _('Games')

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def get_queryset(self):
        if self.bought:
            return self.request.user.profile.get_bought_games()
        else:
            return Game.objects.all()


class GameBuyView(LoginRequiredMixin, DetailView, FormView):  # TODO: Implement payments
    login_url = reverse_lazy('login')
    form_class = GameBuyForm
    model = Game
    context_object_name = 'game'
    template_name = 'game_buy.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.success_url = reverse_lazy('game:detail', kwargs=self.kwargs)
        t = Transaction(
            user=self.request.user.profile,
            game=self.get_object(),
            status=Transaction.SUCCESS_STATUS
        )
        t.save()
        return super(GameBuyView, self).form_valid(form)


class GameDetailView(DetailView):
    model = Game
    context_object_name = 'game'
    template_name = 'game_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = self.request.user.profile
            if user_profile.is_developer and user_profile == self.get_object().dev:
                context['game_stat'] = Transaction.objects.filter(game=self.get_object()) \
                    .aggregate(amount_earned=Sum('amount'), first_sell=Min('datetime'))
        return context


class GameCreateView(LoginRequiredMixin, CreateView):
    fields = ('name', 'slug', 'url', 'icon', 'description', 'price')
    login_url = reverse_lazy('login')
    model = Game
    template_name = 'game_create_view.html'
    success_url = reverse_lazy('profile:user-profile')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.profile.is_developer:
            return HttpResponseForbidden()
        return super(GameCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        import ipdb; ipdb.set_trace()
        context = super(GameCreateView, self).get_context_data(**kwargs)
        context['game_screenshot_forms'] = GameScreenshotModelFormSet()
        return context

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

        return super(GameCreateView, self).form_valid(form)


class GameDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Game
    success_url = reverse_lazy('profile:user-profile')
    template_name = 'game_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(GameDeleteView, self).get_object(queryset=queryset)
        if not obj.dev == self.request.user.profile:
            return HttpResponseForbidden()
        return obj

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_published = not self.object.is_published
        self.object.save()
        return HttpResponseRedirect(success_url)
