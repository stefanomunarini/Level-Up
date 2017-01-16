from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from games.models import Game


def get_upload_path(instance, filename):
    if isinstance(instance, UserProfile):
        return "user_{}/profile_pics/{}".format(instance.user.username, filename)


# Tie the UserProfile to the built-in User model
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class UserProfile(models.Model):
    DEVELOPER_GROUP = 'Developers'
    PLAYER_GROUP = 'Players'

    # Extend django.contrib.auth.models.user
    user = models.OneToOneField(User)

    # Natural language name for the player or the developer, e.g. ‘John Doe’, ‘ZombieSlayer99’ or ‘Samurai Games’
    display_name = models.CharField(_('Display name'), max_length=50, unique=True)
    # A profile picture for the user or a logo for the developer
    profile_picture = models.URLField(_('Profile picture'), null=True, blank=True)

    # End date for limited time bans
    deactivated_until = models.DateTimeField(null=True, blank=True)
    # A field to tie a 3rd party service to this user
    third_party_login = models.CharField(max_length=32, null=True, blank=True)

    """
    Developers only
    """
    # A slug to be used in the developer page url
    url_slug = models.SlugField(_('URL slug'), unique=True, null=True, blank=True)
    # A public link to the developer website for the developer page
    website = models.URLField(_('Developer website'), null=True, blank=True)
    # A support email address that is shown to the players that have bought the developer’s games
    support_email = models.EmailField(_('Developer support email'), null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def is_developer(self):
        if self.user.groups.filter(name=self.DEVELOPER_GROUP).exists():
            return True
        return False

    # Return all the games that this user has bought
    def get_bought_games(self):
        return Game.objects.filter(
            id__in=self.transactions.values_list('game', flat=True)
        )
