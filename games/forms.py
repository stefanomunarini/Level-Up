from django.forms import modelformset_factory, Form, ModelForm, HiddenInput, CharField, ChoiceField, Select
from django.utils.translation import ugettext_lazy as _

from games.models import GameScreenshot, Game


class GameScreenshotModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.game = kwargs.pop('game', None)
        super(GameScreenshotModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GameScreenshot
        fields = ('image',)
        widgets = {'game': HiddenInput()}


GameScreenshotModelFormSet = modelformset_factory(
    model=GameScreenshot,
    form=GameScreenshotModelForm,
    extra=3,
    min_num=0,
    max_num=3
)


class GameUpdateModelForm(ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'icon', 'price', 'description', 'url',)


class GameSearchForm(Form):
    ACCEPTED_CATEGORIES = list(Game.CATEGORIES)
    ACCEPTED_CATEGORIES.insert(0, (None, '-------'))
    ACCEPTED_CATEGORIES = tuple(ACCEPTED_CATEGORIES)

    q = CharField(label=_('Search'), max_length=200, required=False)
    category = ChoiceField(label=_('Category'), choices=ACCEPTED_CATEGORIES, widget=Select, required=False)
