from __future__ import unicode_literals

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import pre_social_login
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User, Group
from django.core import validators
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from games.models import Game
from transactions.models import Transaction


class UserProfile(models.Model):
    DEVELOPER_GROUP = 'Developers'
    PLAYER_GROUP = 'Players'

    # Extend django.contrib.auth.models.user
    user = models.OneToOneField(User, related_name='profile')

    # Natural language name for the player or the developer, e.g. ‘John Doe’, ‘ZombieSlayer99’ or ‘Samurai Games’
    display_name = models.CharField(_('Name'), max_length=50, unique=True)
    # A profile picture for the user or a logo for the developer
    profile_picture = CloudinaryField(
        _('Profile picture'), null=True, blank=True, default='image/upload/v1485194129/default/Ninja-icon.jpg'
    )
    # End date for limited time bans
    deactivated_until = models.DateTimeField(null=True, blank=True)
    # A field to tie a 3rd party service to this user
    third_party_login = models.CharField(max_length=32, null=True, blank=True)

    """
    Developers only
    """
    # A slug to be used in the developer page url
    url_slug = models.SlugField(_('URL slug'),
                                unique=True, null=True, blank=True,
                                validators=[validators.MinLengthValidator(2), validators.MaxLengthValidator(16)],
                                help_text=_('This will be a part of the address of your public page \
                                    and cannot be changed later.'))
    # A public link to the developer website for the developer page
    website = models.URLField(_('Developer website'), null=True, blank=True)
    # A support email address that is shown to the players that have bought the developer’s games
    support_email = models.EmailField(_('Developer support email'), null=True, blank=True,
                                      help_text=_('Visible to those users that have bought your games'))

    def __str__(self):
        return self.display_name

    @property
    def is_developer(self):
        if self.user.groups.filter(name=self.DEVELOPER_GROUP).exists():
            return True
        return False

    # Return all the games that this user has bought
    def get_bought_games(self):
        return Game.objects.filter(
            id__in=self.transactions.filter(status=Transaction.SUCCESS_STATUS).values_list('game', flat=True)
        )

    # Return all the games that this user has developed
    def get_developed_games(self):
        if self.is_developer:
            return Game.objects.filter(dev=self).order_by('-plays', '-downloads', '-name')
        return None

# @receiver(user_signed_up)
# def CreateProfile(sender, request, user, **kwargs):
#     print('user', user)
#     social_profile = SocialAccount.objects.get(user_id=user.id)
#     # group = Group.objects.get(pk=1)
#     # user.groups.set([group])
#     # user.save()
#     UserProfile.objects.create(
#         user=user,
#         third_party_login=social_profile.provider
#     )
#
# @receiver(pre_social_login)
# def PreLogin(sender, request, sociallogin, **kwargs):
#     print('user', sociallogin)