from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView

from games.forms import GameScreenshotModelFormSet
from games.models import Game
from users.models import UserProfile


class GameDetailView(DetailView):
    model = Game
    context_object_name = 'game'
    template_name = 'game_detail_view.html'


class GameCreateView(LoginRequiredMixin, CreateView):
    fields = ('name', 'slug', 'url', 'icon', 'description', 'price')
    login_url = reverse_lazy('profile:login')
    model = Game
    template_name = 'game_create_view.html'
    success_url = reverse_lazy('profile:user-profile')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.userprofile.is_developer():
            return HttpResponseForbidden()
        return super(GameCreateView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(GameCreateView, self).get_context_data(**kwargs)
        context['game_screenshot_forms'] = GameScreenshotModelFormSet()
        return context

    def form_valid(self, form):
        game = form.instance
        game.dev = UserProfile.objects.get(id=self.request.session.get('user_profile_id'))
        game.save()
        game_screenshot_formset = GameScreenshotModelFormSet(self.request.POST,
                                                             self.request.FILES)
        game_screenshot_instances = game_screenshot_formset.save(commit=False)
        for game_screenshot_instance in game_screenshot_instances:
            game_screenshot_instance.game = game
            game_screenshot_instance.save()
        return super(GameCreateView, self).form_valid(form)


class GameDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('profile:login')
    model = Game
    success_url = reverse_lazy('profile:user-profile')
    template_name = 'game_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(GameDeleteView, self).get_object(queryset=queryset)
        if not obj.dev == self.request.user.userprofile:
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
