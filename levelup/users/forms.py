from django.contrib.auth.models import User
from django.forms import ModelForm, Form, CharField, PasswordInput, EmailField

from users.models import UserProfile


class LoginForm(Form):
    username = CharField(label='Username')
    password = CharField(label='Password', widget=PasswordInput())


class UserModelForm(ModelForm):

    confirm_password = CharField(label='Confirm Password', widget=PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
    # username = CharField(label='Username')
    # password = CharField(label='Password', widget=PasswordInput())
    # password_confirm = CharField(label='Confirm Password', widget=PasswordInput())
    # email = EmailField()


class UserProfileModelForm(ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('deactivated_until', 'user',)
