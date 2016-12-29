from django.contrib.auth.models import User
from django.forms import ModelForm, Form, CharField, PasswordInput, EmailField, ChoiceField, modelformset_factory

from users.models import UserProfile


class LoginForm(Form):
    username = CharField(label='Username')
    password = CharField(label='Password', widget=PasswordInput())


class RegistrationUserModelForm(ModelForm):
    confirm_password = CharField(label='Confirm Password', widget=PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class RegistrationUserProfileModelForm(ModelForm):
    PLAYER_SLUG = 'player'
    DEVELOPER_SLUG = 'developer'

    class Meta:
        model = UserProfile
        exclude = ('deactivated_until', 'user', 'third_party_login')

    user_type = ChoiceField(choices=((PLAYER_SLUG, 'Player'),
                                     (DEVELOPER_SLUG, 'Developer'),))


class UserUpdateModelForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UserProfileUpdateModelForm(ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('deactivated_until', 'user', 'third_party_login')


UserProfileUpdateModelFormset = modelformset_factory(
    model=UserProfile,
    form=UserProfileUpdateModelForm,
    extra=1,
    min_num=1,
    max_num=1
)
