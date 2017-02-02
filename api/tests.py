import uuid

from django.contrib.auth.models import User, Group
from django.test import Client
from django.test import TestCase

# Create your tests here.
from django.urls import reverse_lazy

from api import services
from api.models import ApiToken
from games.models import Game
from transactions.models import Transaction
from users.models import UserProfile


class ApiTest(TestCase):
    fixtures = ['groups.json']
    userprofile = None

    def setUp(self):
        group = Group.objects.get(pk=1)
        user = User.objects.create_user(username='api_test_user')
        user.groups.set([group])
        user.save()
        self.userprofile = UserProfile.objects.create(user=user)
        for i in range(100):
            game = Game.objects.create(slug='test'+str(i), dev=self.userprofile, url='http://www.test.com',
                                       description='', price=2.5)
            Transaction.objects.create(user=self.userprofile, game=game, amount=game.price,
                                       status=Transaction.SUCCESS_STATUS)

        self.api_token = ApiToken.objects.create(developer=self.userprofile, token=str(uuid.uuid4()),
                                                 website_url='http://127.0.0.1')

        self.client = Client()

    def test_developer_earnings(self):
        self.assertIsNotNone(self.userprofile.get_developed_games())
        stats = services.get_sale_stats(self.userprofile)
        earnings = stats.get('earnings')
        games = stats.get('games_developed')
        games_earnings = 0
        for game in games:
            games_earnings += game.get('earnings')
        self.assertEqual(earnings, games_earnings)

    def test_api_call_without_token(self):
        response = self.client.get(reverse_lazy('api:developed-games'))
        self.assertEqual(response.status_code, 401)

        response = self.client.get(reverse_lazy('api:sales-stats'))
        self.assertEqual(response.status_code, 401)

        response = self.client.get(reverse_lazy('api:game-stats', kwargs={'slug': Game.objects.first().slug}))
        self.assertEqual(response.status_code, 401)

    def test_api_call_with_token(self):
        response = self.client.get(reverse_lazy('api:developed-games'), HTTP_TOKEN='Bearer ' + self.api_token.token,
                                   HTTP_REFERER=self.api_token.website_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse_lazy('api:sales-stats'), HTTP_TOKEN='Bearer ' + self.api_token.token,
                                   HTTP_REFERER=self.api_token.website_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse_lazy('api:game-stats', kwargs={'slug': Game.objects.first().slug}),
                                   HTTP_TOKEN='Bearer ' + self.api_token.token,
                                   HTTP_REFERER=self.api_token.website_url)
        self.assertEqual(response.status_code, 200)
