import uuid
from _md5 import md5

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Sum, Min
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView
from django.views.generic import UpdateView

from games.forms import GameBuyForm, GameScreenshotModelFormSet, GameUpdateModelForm
from games.models import Game
from levelup.settings import PAYMENT_SERVICE_SELLER_ID, PAYMENT_SERVICE_SECRET_KEY, DEBUG, HEROKU_HOST
from levelup.services import _annotate_downloads
from transactions.models import Transaction


class GameListView(ListView):
    """
    A view that is used whenever a list of games needs to be shown
    Games to be displayed are controlled by passing attribute values in the url dispatcher
    """
    context_object_name = 'games'
    template_name = 'game_list.html'
    bought = False  # Display only games that the user has bought
    page_title = _('Games')
    paginate_by = 20
    paginate_orphans = 3

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def get_queryset(self):
        if self.bought:
            return self.request.user.profile.get_bought_games()
        else:
            return _annotate_downloads(Game.objects.filter(is_published=True), only_positive_downloads=False)


class GameBuyView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    form_class = GameBuyForm
    model = Game
    context_object_name = 'game'
    template_name = 'game_buy.html'

    def dispatch(self, request, *args, **kwargs):
        game = get_object_or_404(Game, slug=kwargs.get(self.slug_url_kwarg))
        if Transaction.objects.filter(user=self.request.user.profile,
                                      game=game,
                                      status=Transaction.SUCCESS_STATUS).exists():
            return HttpResponseRedirect(
                reverse_lazy('game:detail', kwargs={'slug': self.kwargs.get(self.slug_url_kwarg)}))
        return super(GameBuyView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GameBuyView, self).get_context_data(**kwargs)

        pid = self.object.slug
        sid = PAYMENT_SERVICE_SELLER_ID
        amount = self.object.price
        secret_key = PAYMENT_SERVICE_SECRET_KEY
        checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)

        m = md5(checksumstr.encode("ascii"))
        checksum = m.hexdigest()

        # dinamically build the url so it works for both dev and prod
        webapp_url = self.request.is_secure() and 'https://' or 'http://'
        webapp_url += self.request.META['HTTP_HOST']

        redirect_url = webapp_url + reverse('transactions:result')

        context['pid'] = pid
        context['sid'] = sid
        context['amount'] = amount
        context['checksum'] = checksum
        context['success_url'] = redirect_url
        context['cancel_url'] = redirect_url
        context['error_url'] = redirect_url

        return context


class GameDetailView(DetailView):
    model = Game
    context_object_name = 'game'
    template_name = 'game_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = self.request.user.profile
            if user_profile.is_developer and user_profile == self.get_object().dev:
                context['game_stats'] = Transaction.objects.filter(game=self.get_object(),
                                                                  status=Transaction.SUCCESS_STATUS) \
                    .aggregate(amount_earned=Sum('amount'), first_sell=Min('datetime'))
        return context


class GameCreateView(LoginRequiredMixin, CreateView):
    fields = ('name', 'slug', 'url', 'icon', 'description', 'price')
    login_url = reverse_lazy('login')
    model = Game
    template_name = 'game_create.html'
    success_url = reverse_lazy('profile:user-profile')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.profile.is_developer:
            return HttpResponseForbidden()
        return super(GameCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
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


class GameUpdateView(LoginRequiredMixin, UpdateView):
    model = Game
    context_object_name = 'game'
    form_class = GameUpdateModelForm
    login_url = reverse_lazy('login')
    template_name = 'game_update.html'

    def get_object(self, queryset=None):
        self.object = super(GameUpdateView, self).get_object(queryset)
        if self.object not in self.request.user.profile.get_developed_games():
            raise PermissionDenied
        return self.object

    def get_success_url(self):
        return reverse_lazy('game:detail', kwargs={'slug': self.object.slug})


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
