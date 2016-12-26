import os

from django.db import models
from django.db.models import Q

from levelup.settings import BASE_DIR
from users.models import UserProfile


def get_upload_path(instance, filename):
    if isinstance(instance, Game):
        return "dev_{}/game_{}/{}".format(instance.dev.dev_slug, instance.slug, filename)
    if isinstance(instance, GameScreenshot):
        return "dev_{}/game_{}/{}".format(instance.game.dev.dev_slug, instance.game.slug, filename)


class Game(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(null=False, blank=False)
    dev = models.ForeignKey(UserProfile,
                            on_delete=models.CASCADE,
                            limit_choices_to=Q(groups__name='Developers'),
                            related_name='games')
    url = models.URLField(null=False, blank=False)
    icon = models.ImageField(null=True, blank=True, upload_to=get_upload_path, max_length=500)
    description = models.TextField()
    price = models.FloatField(null=False, blank=False)
    is_public = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class GameScreenshot(models.Model):
    image = models.ImageField(null=False, blank=False, upload_to=get_upload_path, max_length=500)
    game = models.ForeignKey(Game, related_name='screenshots')


class GameScore(models.Model):
    player = models.ForeignKey(UserProfile, related_name='scores')
    game = models.ForeignKey(Game, related_name='scores')
    start_time = models.DateTimeField(auto_now_add=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
