from django.http import JsonResponse
from django.views import View

from api import services
from users.models import ApiToken


class ApiBaseView(View):

    def dispatch(self, request, *args, **kwargs):
        token = request.META.get('HTTP_TOKEN')
        bearer = token.split(' ')[0]
        token_value = token.split(' ')[1]
        request_origin = self.request.is_secure() and 'https://' or 'http://' + self.request.META['HTTP_HOST']
        self.api_toke_obj = ApiToken.objects.filter(token=token_value, website_url=request_origin)
        if not bearer == 'Bearer' and not self.api_toke_obj.exists():
            return JsonResponse(data={'error': 'Unauthorized'}, status=401)
        return super(ApiBaseView, self).dispatch(request, *args, **kwargs)
        # return JsonResponse(data={'status': 'Yes'}, status=200)


class MyDevelopedGames(ApiBaseView):
    def dispatch(self, request, *args, **kwargs):
        super(MyDevelopedGames, self).dispatch(request, *args, **kwargs)
        response = {
            'games': services.get_developed_games(self.api_toke_obj)
        }
        return JsonResponse(data=response, status=200)
