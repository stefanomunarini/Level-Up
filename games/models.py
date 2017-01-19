from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


def get_upload_path(instance, filename):
    if isinstance(instance, Game):
        return "dev_{}/game_{}/{}".format(instance.dev.url_slug, instance.slug, filename)
    if isinstance(instance, GameScreenshot):
        return "dev_{}/game_{}/screenshots/{}".format(instance.game.dev.url_slug, instance.game.slug, filename)


class Game(models.Model):
    name = models.CharField(_('Game name'), max_length=64)
    slug = models.SlugField(_('Game URL slug'),
                            help_text=_('Part of the game page address on LevelUp, cannot be changed later'),
                            null=False, blank=False, unique=True)
    dev = models.ForeignKey('users.UserProfile',
                            on_delete=models.CASCADE,
                            limit_choices_to=Q(groups__name='Developers'),
                            related_name='games')
    url = models.URLField(_('Source URL'), help_text=_('Where is the game hosted?'), null=False, blank=False)
    icon = models.URLField(null=True, blank=True)
    description = models.TextField()
    price = models.FloatField(null=False, blank=False)
    is_public = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


class GameScreenshot(models.Model):
    image = CloudinaryField('image')
    game = models.ForeignKey(Game, related_name='screenshots')


class GameScore(models.Model):
    player = models.ForeignKey('users.UserProfile', related_name='scores')
    game = models.ForeignKey(Game, related_name='scores')
    start_time = models.DateTimeField(auto_now_add=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
