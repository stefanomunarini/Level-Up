from django.http import Http404
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import DetailView

from api import services
from api.forms import ApiBaseForm
from api.models import ApiToken
from games.models import Game


class ApiBaseView(View):
    form_class = ApiBaseForm
    http_method_names = ('GET',)

    INVALID_TOKEN_MESSAGE = _(
        'Unauthorized! The token you are trying to use is invalid. Format should be: Bearer <TOKEN>')

    def dispatch(self, request, *args, **kwargs):
        # the parameter is only 'TOKEN' but it is automatically attached with 'HTTP_', hence 'HTTP_TOKEN'
        token = request.META.get('HTTP_TOKEN')
        if not token or not len(token.split(' ')) == 2 or 'Bearer' not in token:
            return JsonResponse(data={'error': self.INVALID_TOKEN_MESSAGE}, status=401)
        self.form = self.form_class({
            'token': token.split(' ')[1],
            'website_url': request.META.get('HTTP_REFERER', '')
        })
        if self.form.is_valid():
            self.api_token_obj = self.form.instance
            return self.request_valid()
        else:
            return self.request_invalid()

    def request_valid(self):
        raise NotImplementedError('You must implement this function, which is responsible for returning the response.')

    def request_invalid(self, errors=None):
        if not errors:
            errors = self.form.errors
        return JsonResponse(data={'errors': errors},
                            status=401)


class ApiDevelopedGamesView(ApiBaseView):
    def request_valid(self):
        response = {
            'games': services.get_developed_games(self.api_token_obj)
        }
        return JsonResponse(data=response, status=200)


class ApiSaleStatsView(ApiBaseView):
    def request_valid(self):
        response = {
            'stats': services.get_sale_stats(self.api_token_obj.developer)
        }
        return JsonResponse(data=response, status=200)


class ApiGameStatsView(ApiBaseView, DetailView):
    model = Game

    def dispatch(self, request, *args, **kwargs):
        """
        Override the dispatcher so we can return a JSON message error if no game
        is found with the requested <slug>
        """
        try:
            dispatcher = super(ApiGameStatsView, self).dispatch(request, *args, **kwargs)
        except Http404 as error:
            return self.request_invalid(errors=error.args)
        else:
            return dispatcher

    def request_valid(self):
        response = {
            'game': self.get_object().name
        }
        return JsonResponse(data=response, status=200)
