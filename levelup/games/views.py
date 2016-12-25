from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView

from games.models import Game
from users.models import UserProfile


class GameCreateView(LoginRequiredMixin, CreateView):
    fields = ('name', 'slug', 'url', 'icon', 'description', 'price')
    model = Game
    template_name = 'game_create_view.html'
    success_url = reverse_lazy('profile:user-profile')

    def form_valid(self, form):
        game = form.instance
        game.dev = UserProfile.objects.get(id=self.request.session.get('user_profile_id'))
        game.save()
        return super(GameCreateView, self).form_valid(form)


class GameDeleteView(LoginRequiredMixin, DeleteView):
    model = Game
    success_url = reverse_lazy('profile:user-profile')
    template_name = 'game_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(GameDeleteView, self).get_object(queryset=queryset)
        if not obj.dev == self.request.user.userprofile:
            raise HttpResponseForbidden
        return obj
