from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView

from . import services


class HomepageView(TemplateView):
    elements_to_show = 6  # the number of games to show for every section
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['form'] = AuthenticationForm()
        context.update(services.get_homepage_games(self.elements_to_show))
        return context
