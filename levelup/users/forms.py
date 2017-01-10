from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import password_validation
from django import forms
from django.forms import (
    Form, ModelForm, BaseModelForm,
    BooleanField, CharField, ChoiceField, EmailField, FileField, URLField, SlugField,
    PasswordInput,
    modelformset_factory,
)
from django.forms.models import model_to_dict, fields_for_model
from django.utils.translation import ugettext_lazy as _

from users.models import UserProfile, PlayerProfile, DeveloperProfile

class SignupUserForm(Form, BaseModelForm):    
    username = UsernameField(label=_('Username'))
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
        #self.instance.username = self.cleaned_data.get('username')
        #password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2
    
    def clean(self):
        data = super(SignupUserForm, self).clean()
        return data
    
    def save(self, *args, **kwargs):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
        )
        user.save()
        self.instance.user = user
        self.instance.user_id = user.id
        data = super(SignupUserForm, self).save(*args,**kwargs)
        return data    

class SignupPlayerForm(ModelForm, SignupUserForm):
    field_order = ('username', 'password1', 'password2')
    class Meta:
        model = PlayerProfile
        fields = ('display_name', 'profile_picture')

class SignupDeveloperForm(ModelForm, SignupUserForm):
    field_order = ('username', 'password1', 'password2')
    class Meta:
        model = DeveloperProfile
        fields = ('display_name', 'profile_picture', 'url_slug', 'website', 'support_email')
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

"""
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
"""
# This class combines User and UserProfile models to create a single form
# http://stackoverflow.com/a/15892615
class SignupForm(ModelForm):
    
    confirm_email = EmailField(label=_('Confirm Email'),required=False)
    confirm_password = CharField(label=_('Confirm Password'),required=False,widget=PasswordInput())
    is_developer = BooleanField(label=_('I’m a developer!'),required=False)
    
    def __init__(self, instance=None, *args, **kwargs):
        _fields = ('username', 'password', 'email', 'first_name', 'last_name',)
        #_initial = model_to_dict(instance.user, _fields) if instance is not None else {}
        _initial = {}
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields.update(fields_for_model(User, _fields))
        self.order_fields((
            'profile_pic', 'first_name', 'last_name', 'username',
            'email', 'confirm_email',
            'password', 'confirm_password',
            'is_developer', 'dev_name', 'dev_email_support', 'dev_website',
        ))
        self.fields['profile_pic'].required = False
        self.fields['email'].required = True

    class Meta:
        model = UserProfile
        exclude = ('user','deactivated_until','third_party_login')

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.username = self.cleaned_data['username']
        u.password = self.cleaned_data['password']
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(SignupForm, self).save(*args,**kwargs)
        return profile
    
    def clean_confirm_email(self):
        val = self.cleaned_data['confirm_email']
        # Check if main field is valid and only then check confirmation field
        if 'email' in self.cleaned_data and val != self.cleaned_data['email']:
            raise forms.ValidationError(_('The account emails don’t match.'))
        return val
    
    def clean_confirm_password(self):
        val = self.cleaned_data['confirm_password']
        # Check if main field is valid and only then check confirmation field
        if 'password' in self.cleaned_data and val != self.cleaned_data['password']:
            raise forms.ValidationError(_('The passwords don’t match.'))
        return val

class SignupUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class SignupUserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('deactivated_until', 'user', 'third_party_login')







class SignupPlayerUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {'username': _('Email address'),}
        field_classes = {'username': EmailField,}
        help_texts = {'username': _(''),}
        widgets = {'password': PasswordInput(),}
    
    def save(self, *args, **kwargs):
        user = super(SignupForm, self).save(*args,**kwargs)
        return user

class SignupDevUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'username')
        field_classes = {'username':SlugField,}
        labels = {'username':_('Developer Slug'),}
        help_texts = {'username':_('Cannot be changed later'),}
        widgets = {'password': PasswordInput(),}
    
    def save(self, *args, **kwargs):
        user = super(SignupForm, self).save(*args,**kwargs)
        return user

class SignupPlayerProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('display_name','profile_pic',)

class SignupDevProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('display_name', 'dev_website', 'dev_email_support', 'profile_pic')


"""