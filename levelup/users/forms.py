from django.forms import ModelForm

from users.models import UserProfile


class UserProfileModelForm(ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('deactivated_until',)
