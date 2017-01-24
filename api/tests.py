from django.contrib.auth.models import User, Group
from django.test import TestCase

# Create your tests here.
from api import services
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
            game = Game.objects.create(slug='test'+str(i), dev=self.userprofile, url='http://www.test.com', description='', price=2.5)
            Transaction.objects.create(user=self.userprofile, game=game, amount=game.price, status=Transaction.SUCCESS_STATUS)

    def test_developer_earnings(self):
        self.assertIsNotNone(self.userprofile.get_developed_games())
        stats = services.get_sale_stats(self.userprofile)
        earnings = stats.get('earnings')
        games = stats.get('games_developed')
        games_earnings = 0
        for game in games:
            games_earnings += game.get('earnings')
        self.assertEqual(earnings, games_earnings)
