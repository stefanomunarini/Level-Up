from django.db import models
from django.db.models import Q

from users.models import UserProfile


class Game(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(null=False, blank=False)
    dev = models.ForeignKey(UserProfile,
                            on_delete=models.CASCADE,
                            limit_choices_to=Q(groups__name='Developers'),
                            related_name='games')
    url = models.URLField(null=False, blank=False)
    icon = models.ImageField(null=True, blank=True)
    description = models.TextField()
    price = models.FloatField(null=False, blank=False)
    is_public = models.BooleanField(default=True)


class GameScreenshot(models.Model):
    image = models.ImageField(null=False, blank=False)
    game = models.ForeignKey(Game, related_name='screenshots')


class GameScore(models.Model):
    player = models.ForeignKey(UserProfile, related_name='scores')
    game = models.ForeignKey(Game, related_name='scores')
    start_time = models.DateTimeField(auto_now_add=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

