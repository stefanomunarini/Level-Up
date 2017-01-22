from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class GameOwnershipRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        dispatcher = super(GameOwnershipRequiredMixin, self).dispatch(request, *args, **kwargs)
        self.object = self.get_object()
        if self.object not in request.user.profile.get_bought_games():
            messages.error(request,
                           'Hey {}, you must buy the game before being able to play!'.format(request.user.profile))
            return HttpResponseRedirect(reverse_lazy('game:buy', kwargs={'slug': self.object.slug}))
        return dispatcher