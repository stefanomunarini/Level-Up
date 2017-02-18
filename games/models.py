from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models import Q, Count
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from transactions.models import Transaction


class GameManager(models.Manager):
    def get_queryset(self):
        return super(GameManager, self).get_queryset() \
            .annotate(downloads=Count('transactions', distinct=True)) \
            .annotate(plays=Count('scores', distinct=True))


class Game(models.Model):

    ACTION_CATEGORY = 'action'
    ADVENTURE_CATEGORY = 'adventure'
    ARCADE_CATEGORY = 'arcade'
    KIDS_CATEGORY = 'kids'
    RPG_CATEGORY = 'rpg'
    SPORT_CATEGORY = 'sport'
    STRATEGY_CATEGORY = 'strategy'

    CATEGORIES = (
        (ACTION_CATEGORY, _('Action')),
        (ADVENTURE_CATEGORY, _('Adventure')),
        (ARCADE_CATEGORY, _('Arcade')),
        (KIDS_CATEGORY, _('Kids')),
        (RPG_CATEGORY, _('RPG')),
        (SPORT_CATEGORY, _('Sport')),
        (STRATEGY_CATEGORY, _('Strategy')),
    )

    name = models.CharField(_('Game name'), max_length=64, db_index=True)
    slug = models.SlugField(_('Game URL slug'),
                            help_text=_('Part of the game page address on LevelUp, cannot be changed later'),
                            null=False, blank=False, unique=True)
    dev = models.ForeignKey('users.UserProfile',
                            on_delete=models.CASCADE,
                            limit_choices_to=Q(groups__name='Developers'),
                            related_name='games')
    url = models.URLField(_('Source URL'), help_text=_('Where is the game hosted?'), null=False, blank=False)
    icon = CloudinaryField(_('Game icon'),)
    description = models.TextField(db_index=True)
    price = models.FloatField(null=False, blank=False)
    is_public = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now, blank=True)

    category = models.CharField(max_length=31, choices=CATEGORIES, null=False, blank=False)

    """
    Override default manager so that the default queryset include two extra attributes:
    - downloads: the number of download for a particular game (which is the number of Transactions)
    - plays: the number of times the game has been played (which is the number of GameScores)
    """
    objects = GameManager()

    def __str__(self):
        return self.name


class GameScreenshot(models.Model):
    image = CloudinaryField(_('Screenshot'))
    game = models.ForeignKey(Game, related_name='screenshots')


class GameScore(models.Model):
    player = models.ForeignKey('users.UserProfile', related_name='scores')
    game = models.ForeignKey(Game, related_name='scores')
    timestamp = models.DateTimeField(default=timezone.now, blank=True)
    score = models.IntegerField(null=True, blank=True)


class GameState(models.Model):
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now, blank=True)
    state = models.CharField(max_length=256)
