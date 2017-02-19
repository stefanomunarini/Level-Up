# Create your tests here.

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse_lazy

from api.models import ApiToken
from users.forms import UserUpdateModelForm, UserProfileUpdateModelForm

class UserTest(TestCase):
    fixtures = ['groups.json', 'test_user.json']

    def setUp(self):
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
        users = User.objects.all()  # a, s, q, w
        self.userA = users[0]  # player
        self.userS = users[1]  # player
        self.userQ = users[2]  # developer
        self.userW = users[3]  # developer

        self.playerA_client = Client()
        self.playerA_client.login(username=self.userA.username, password='test')

        self.devQ_client = Client()
        self.devQ_client.login(username=self.userQ.username, password='test')

    def test_player_dev_action_buttons(self):
        url = reverse_lazy('profile:user-profile')

        response = self.devQ_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="update-profile"')
        self.assertContains(response, 'id="add-api-token"')

        response = self.playerA_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="update-profile"')
        self.assertNotContains(response, 'id="add-api-token"')

    def test_update_own_profile(self):
        url = reverse_lazy('profile:user-profile-update')

        response = self.devQ_client.get(url)
        self.assertContains(response, '<a href="/profile/">q@mail.com</a>')

        response = self.playerA_client.get(url)
        self.assertContains(response, '<a href="/profile/">a@mail.com</a>')

        data = {
            'website': 'http://dev-q.site.com',
            'support_email': 'support@mail.com',
            'display_name': 'Phu',
        }
        response = self.devQ_client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/profile/")
        updated_user = User.objects.filter(pk=self.userQ.id)[0]
        self.assertEqual(updated_user.profile.display_name, "Phu")
        self.assertEqual(updated_user.profile.website, "http://dev-q.site.com")
        self.assertEqual(updated_user.profile.support_email, "support@mail.com")

    def test_add_api_key(self):
        url = reverse_lazy('profile:create-api-key')

        response = self.devQ_client.post(url, {'website_url': 'example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/profile/")

        # import ipdb; ipdb.set_trace()
        new_key = ApiToken.objects.first()
        self.assertIn('example.com', new_key.website_url)
        self.assertEqual(new_key.developer, self.userQ.profile)

        response = self.playerA_client.post(url, {'website_url': 'example.com'})
        self.assertEqual(response.status_code, 403)

    def test_delete_api_key(self):
        add_url = reverse_lazy('profile:create-api-key')
        self.devQ_client.post(add_url, {'website_url': 'test.com'})
        new_key = ApiToken.objects.first()
        delete_url = reverse_lazy('profile:delete-api-key', kwargs={'pk': new_key.pk})
        response = self.devQ_client.post(delete_url, {})
        self.assertEqual(response.status_code, 302)

        self.devQ_client.post(add_url, {'website_url': 'test.com'})
        new_key = ApiToken.objects.first()
        delete_url = reverse_lazy('profile:delete-api-key', kwargs={'pk': new_key.pk})
        response = self.playerA_client.post(delete_url, {})
        self.assertEqual(response.status_code, 403)
