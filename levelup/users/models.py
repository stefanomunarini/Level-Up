from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.db import models

from games.models import Game
from transactions.models import Transaction

def get_upload_path(instance, filename):
    if isinstance(instance, UserProfile):
        return "user_{}/profile_pics/{}".format(instance.user.username, filename)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class UserProfile(models.Model):

    DEVELOPER_GROUP = 'Developers'
    PLAYER_GROUP = 'Players'

    # Extend django.contrib.auth.models.user
    user = models.OneToOneField(User)
    
    # public stuff
    display_name = models.CharField(_('Display name'), max_length=50, unique=True)
    profile_picture = models.ImageField(_('Profile picture'), null=True, blank=True, upload_to=get_upload_path, max_length=255)
    
    
    # hidden stuff
    deactivated_until = models.DateTimeField(null=True, blank=True)
    third_party_login = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def is_developer(self):
        if self.user.groups.filter(name=self.DEVELOPER_GROUP).exists():
            return True
        return False
    
    def bought_games(self):
        return Game.objects.filter(
            id__in=Transaction.objects.filter(
                user=self,
                status=Transaction.SUCCESS_STATUS
            )
        )

class PlayerProfile(UserProfile): pass

class DeveloperProfile(UserProfile): 
    url_slug = models.SlugField(_('URL slug'), unique=True)
    website = models.URLField(_('Developer website'), null=True, blank=True)
    support_email = models.EmailField(_('Developer support email'), null=True, blank=True)