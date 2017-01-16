from django.forms import modelformset_factory, Form, ModelForm, HiddenInput

from games.models import GameScreenshot


class GameScreenshotModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.game = kwargs.pop('game', None)
        # self.queryset = GameScreenshot.objects.none()
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


class GameBuyForm(Form):
    pass