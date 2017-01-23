from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models import Q, Count
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from transactions.models import Transaction


def get_upload_path(instance, filename):
    if isinstance(instance, Game):
        return "dev_{}/game_{}/{}".format(instance.dev.url_slug, instance.slug, filename)
    if isinstance(instance, GameScreenshot):
        return "dev_{}/game_{}/screenshots/{}".format(instance.game.dev.url_slug, instance.game.slug, filename)


class GameManager(models.Manager):
    def get_queryset(self):
        return super(GameManager, self).get_queryset() \
            .annotate(downloads=Count('transactions', distinct=True)) \
            .annotate(plays=Count('scores', distinct=True))


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
    date_added = models.DateTimeField(default=timezone.now, blank=True)

    """
    Override default manager so that the default queryset include two extre attributes:
    - downloads: the number of download for a particular game (which is the number of Transactions)
    - plays: the number of times the game has been played (which is the number of GameScores)
    """
    objects = GameManager()

    def __str__(self):
        return self.name


class GameScreenshot(models.Model):
    image = CloudinaryField('image')
    game = models.ForeignKey(Game, related_name='screenshots')


class GameScore(models.Model):
    player = models.ForeignKey('users.UserProfile', related_name='scores')
    game = models.ForeignKey(Game, related_name='scores')
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)


class GameState(models.Model):
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now, blank=True)
    state = models.CharField(max_length=256)
