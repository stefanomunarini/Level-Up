from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from games.models import Game
from users.models import UserProfile


class GameCreateView(CreateView):
    fields = ('name', 'slug', 'url', 'icon', 'description', 'price')
    model = Game
    template_name = 'game_create_view.html'
    success_url = reverse_lazy('profile:user-profile')

    def form_valid(self, form):
        game = form.instance
        game.dev = UserProfile.objects.get(id=self.request.session.get('user_profile_id'))
        game.save()
        return super(GameCreateView, self).form_valid(form)
