from django.core.exceptions import ValidationError
from django.forms import ModelForm

from api.models import ApiToken


class ApiBaseForm(ModelForm):
    class Meta:
        model = ApiToken
        fields = ('token', 'website_url')

    def clean(self):
        api_token_object = ApiToken.objects.filter(token=self.cleaned_data.get('token'),
                                                   website_url=self.cleaned_data.get('website_url'))
        if not api_token_object.exists():
            raise ValidationError(message='Invalid Token')
        self.instance = api_token_object.first()
        return self.cleaned_data
