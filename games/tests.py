# Create your tests here.
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.test import Client
from django.test import TestCase
from django.urls import reverse_lazy

from games.models import Game
from users.models import UserProfile


class GameTest(TestCase):
    fixtures = ['groups.json']

    def setUp(self):
        username = 'test'
        password = 'test'
        group = Group.objects.get(pk=1)  # developer
        dev_user = User.objects.create_user(username, password=password)
        dev_user_profile = UserProfile.objects.create(display_name=username, user=dev_user)
        dev_user.groups.set([group])
        dev_user_profile.save()
        dev_user.save()

        self.dev_client = Client()
        self.dev_client.login(username=username, password=password)

        username = 'test1'
        password = 'test1'
        another_dev_user = User.objects.create_user(username, password=password)
        another_user_profile = UserProfile.objects.create(display_name=username, user=another_dev_user)
        another_dev_user.groups.set([group])
        another_user_profile.save()
        another_dev_user.save()

        self.another_dev_client = Client()
        self.another_dev_client.login(username=username, password=password)

        username = 'test2'
        password = 'test2'
        group = Group.objects.get(pk=2)  # player
        player_user = User.objects.create_user(username, password=password)
        player_user_profile = UserProfile.objects.create(display_name=username, user=player_user)
        player_user.groups.set([group])
        player_user_profile.save()
        player_user.save()

        self.player_client = Client()
        self.player_client.login(username=username, password=password)

        self.game = Game.objects.create(name=username, slug=username, dev=dev_user_profile, url=username,
                                        description=username, price=1, category=Game.ACTION_CATEGORY)

    def test_create_game_view_permissions(self):
        url = reverse_lazy('game:add')

        self._test_dev_player_responses(url)

    def test_update_game_view_permissions(self):
        url = reverse_lazy('game:update', kwargs={'slug': self.game.slug})

        self._test_dev_player_responses(url)

    def _test_dev_player_responses(self, url):
        response = self.dev_client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.player_client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 403)

    def test_only_owner_can_update_game(self):
        url = reverse_lazy('game:update', kwargs={'slug': self.game.slug})

        response = self.another_dev_client.get(url)
        self.assertEqual(response.status_code, 403)

        response = self.dev_client.get(url)
        self.assertEqual(response.status_code, 200)
