from django import forms
from django.contrib.auth.models import User, Group
from django.forms import (
    ModelForm, modelformset_factory,
)
from django.utils.translation import ugettext_lazy as _

from users.models import UserProfile


# Signup Forms

class AbstractSignupUserForm(ModelForm):
    email = forms.EmailField()
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _('The passwords do not match.'),
                code='password_mismatch',
            )
        return password2

    def clean_email(self):
        username = self.cleaned_data.get('email')
        if User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError(_('This username is already in use.'))
        return username

    def save(self, *args, **kwargs):
        if type(self) is SignupDeveloperForm:
            group = Group.objects.get(pk=1)
        elif type(self) is SignupPlayerForm:
            group = Group.objects.get(pk=2)
        else:
            raise NotImplementedError()

        """
        Create the user to be linked to the UserProfile model
        """
        email = self.cleaned_data['email']
        user = User.objects.create_user(
            username=email,
            password=self.cleaned_data['password1'],
            email=email
        )
        user.groups.set([group])
        user.save()
        self.instance.user = user
        self.instance.user_id = user.id
        return super(AbstractSignupUserForm, self).save(*args, **kwargs)


class SignupPlayerForm(AbstractSignupUserForm):
    field_order = ('email', 'password1', 'password2')

    class Meta:
        model = UserProfile
        fields = ('display_name', 'profile_picture')


class SignupDeveloperForm(AbstractSignupUserForm):
    field_order = ('email', 'password1', 'password2')

    class Meta:
        model = UserProfile
        fields = ('display_name', 'profile_picture', 'url_slug', 'website', 'support_email')


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

"""
class RegistrationUserModelForm(ModelForm):
    confirm_password = CharField(label=_('Confirm Password'), widget=PasswordInput())

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


class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
    
    field_order = ('profile_pic','first_name','last_name','username','email','confirm_email','password','confirm_password')
    
    profile_pic = FileField(label=_('Profile Picture'),required=False)
    
    username = SlugField(
        max_length = 30,
        label=_('Username'), 
        error_messages={'invalid':_('Username can only contain letters, numbers, hyphens and underscores.')}
    )
    
    email = EmailField(label=_('Email'))
    confirm_email = EmailField(label=_('Confirm Email'),required=False)
    
    password = CharField(label=_('Password'),widget=PasswordInput())
    confirm_password = CharField(label=_('Confirm Password'),required=False,widget=PasswordInput())
    
    is_developer = BooleanField(label=_('I’m a developer!'),required=False)
    
    dev_slug = SlugField(label=_('Developer URL slug'),help_text=_('Appears in the url of the developer profile'),required=False)
    dev_email_support = EmailField(label=_('Customer Support Email'),help_text=_('Available for the users that have bought your games'),required=False)
    confirm_dev_email_support = EmailField(label=_('Confirm Support Email'),required=False)
    dev_website = URLField(label=_('Developer Website'),required=False)
    
    def clean_confirm_email(self):
        val = self.cleaned_data['confirm_email']
        # Check if main field is filled and only then check confirmation field
        if 'email' in self.cleaned_data and val != self.cleaned_data['email']:
            raise forms.ValidationError(_('The account emails don’t match.'))
        return val
    
    def clean_confirm_password(self):
        val = self.cleaned_data['confirm_password']
        # Check if main field is filled and only then check confirmation field
        if 'password' in self.cleaned_data and val != self.cleaned_data['password']:
            raise forms.ValidationError(_('The passwords don’t match.'))
        return val
    
    def clean_dev_slug(self):
        val = self.cleaned_data['dev_slug']
        if 'is_developer' in self.data and val == '':
            raise forms.ValidationError(_('This field is required.'))
        return val
    
    def clean_confirm_dev_email_support(self):
        val = self.cleaned_data['confirm_dev_email_support']
        # Check if the user is a developer and that main field is filled and only then check confirmation field
        if 'is_developer' in self.data and 'dev_email_support' in self.cleaned_data and val != self.data['dev_email_support']:
            raise forms.ValidationError(_('The developer support emails don’t match.'))
        return val

"""
