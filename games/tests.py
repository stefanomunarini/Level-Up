# Create your tests here.

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse_lazy

from games.models import Game


class GameTest(TestCase):
    fixtures = ['groups.json', 'test_game.json']

    def setUp(self):
        # Fix the passwords of fixtures
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
        users = User.objects.all()

        developer1 = users[0]  # owner of the game pk=1
        developer2 = users[1]
        player = users[2]  # bought the game pk=1

        self.game = Game.objects.first()

        self.dev_client = Client()
        self.dev_client.login(username=developer1.username, password='developer1')

        self.another_dev_client = Client()
        self.another_dev_client.login(username=developer2.username, password='developer2')

        self.player_client = Client()
        self.player_client.login(username=player.username, password='player')

    def test_create_game_view_permissions(self):
        url = reverse_lazy('game:add')

        self._test_dev_player_responses(url)

    def test_update_game_view_permissions(self):
        url = reverse_lazy('game:update', kwargs={'slug': self.game.slug})

        self._test_dev_player_responses(url)

    def test_delete_game_view_permissions(self):
        url = reverse_lazy('game:delete', kwargs={'pk': self.game.pk})

        self._test_dev_player_responses(url)

    def _test_dev_player_responses(self, url):
        response = self.dev_client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.player_client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 403)

    def test_only_owner_can_update_game(self):
        url = reverse_lazy('game:update', kwargs={'slug': self.game.slug})

        self._test_devs_game_ownership(url)

    def test_only_owner_can_unpublish_game(self):
        url = reverse_lazy('game:delete', kwargs={'pk': self.game.pk})

        self._test_devs_game_ownership(url)

    def _test_devs_game_ownership(self, url):
        response = self.player_client.get(url)
        self.assertEqual(response.status_code, 403)

        response = self.another_dev_client.get(url)
        self.assertEqual(response.status_code, 403)

        response = self.dev_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_only_authorized_users_can_play_game(self):
        url = reverse_lazy('game:play', kwargs={'slug': self.game.slug})

        response = self.player_client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.dev_client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_game_details_contains_edit_button(self):
        url = reverse_lazy('game:detail', kwargs={'slug': self.game.slug})

        response = self.another_dev_client.get(url)
        self.assertNotContains(response, 'edit-game-button')

        response = self.player_client.get(url)
        self.assertNotContains(response, 'edit-game-button')

        response = self.dev_client.get(url)
        self.assertContains(response, 'edit-game-button', status_code=200)

    def test_my_game_list(self):
        url = reverse_lazy('game:my-games')

        response = self.dev_client.get(url)
        self.assertEqual(len(response.context_data.get('games')), 0)

        response = self.another_dev_client.get(url)
        self.assertEqual(len(response.context_data.get('games')), 0)

        response = self.player_client.get(url)
        self.assertEqual(len(response.context_data.get('games')), 1)

    # def test_developer_own_game_list(self):
    #     url = reverse_lazy('profile:user-profile')
    #
    #     response = self.dev_client.get(url)
    #     # import ipdb; ipdb.set_trace()
    #     self.assertEqual(len(response.context_data.get('games')), 1)