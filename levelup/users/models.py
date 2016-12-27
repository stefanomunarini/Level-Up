from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


def get_upload_path(instance, filename):
    if isinstance(instance, UserProfile):
        return "user_{}/profile_pics/{}".format(instance.user.username, filename)


class UserProfile(models.Model):

    DEVELOPER_GROUP = 'Developers'
    PLAYER_GROUP = 'Players'

    # Extend django.contrib.auth.models.user
    user = models.OneToOneField(User)

    deactivated_until = models.DateTimeField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to=get_upload_path, max_length=255)
    third_party_login = models.CharField(max_length=32, null=True, blank=True)

    # developer fields
    dev_slug = models.SlugField(null=True, blank=True)
    dev_website = models.URLField(null=True, blank=True)
    dev_email_support = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def is_developer(self):
        if self.user.groups.filter(name=self.DEVELOPER_GROUP).exists():
            return True
        return False
