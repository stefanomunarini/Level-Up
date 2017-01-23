from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views import View

from api import services
from users.models import ApiToken


class ApiBaseView(View):

    ERROR_MESSAGE = _('error')
    NO_TOKEN_MESSAGE = _('Unauthorized! You need to provide a valid Bearer token to use the APIs.')
    INVALID_TOKEN_MESSAGE = _('Unauthorized! The token you are trying to use is invalid. Format should be: Bearer TOKEN')

    def dispatch(self, request, *args, **kwargs):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            return JsonResponse(data={self.ERROR_MESSAGE: self.NO_TOKEN_MESSAGE}, status=401)
        if not len(token.split(' ')) == 2 or 'Bearer' not in token:
            return JsonResponse(data={self.ERROR_MESSAGE: self.INVALID_TOKEN_MESSAGE}, status=401)
        token_value = token.split(' ')[1]
        request_origin = self.request.is_secure() and 'https://' or 'http://' + self.request.META['HTTP_HOST']
        self.api_toke_obj = ApiToken.objects.filter(token=token_value, website_url=request_origin)
        if not self.api_toke_obj.exists():
            return JsonResponse(data={'error': 'Unauthorized'}, status=401)
        return super(ApiBaseView, self).dispatch(request, *args, **kwargs)


class MyDevelopedGames(ApiBaseView):
    def dispatch(self, request, *args, **kwargs):
        dispatcher = super(MyDevelopedGames, self).dispatch(request, *args, **kwargs)
        if dispatcher.status_code != 200:
            return dispatcher
        response = {
            'games': services.get_developed_games(self.api_toke_obj)
        }
        return JsonResponse(data=response, status=200)
