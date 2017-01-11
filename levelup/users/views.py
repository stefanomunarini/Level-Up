from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView
from django.views.generic.edit import ProcessFormView
from django.utils.translation import ugettext_lazy as _

from games.models import Game
from users.models import UserProfile
from users.forms import (
    SignupPlayerForm, SignupDeveloperForm,
    UserUpdateModelForm, UserProfileUpdateModelForm, UserProfileUpdateModelFormset
)


# User Signup

class AbstractSignupView(FormView):
    """
        This acts as a generic SignupView that is used by SignupPlayerView and SignupDeveloperView
        """
    template_name = 'signup.html'
    success_url = reverse_lazy('profile:user-profile')

    def get(self, request, *args, **kwargs):
        # Don’t allow signups if the user is logged in
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('home'))
        return super(AbstractSignupView, self).get(self, request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        new_user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        login(self.request, new_user)
        return super(AbstractSignupView, self).form_valid(self)


class SignupPlayerView(AbstractSignupView):
    form_class = SignupPlayerForm


class SignupDeveloperView(AbstractSignupView):
    form_class = SignupDeveloperForm


# User Profile

# TODO: I think this is redundant as request.user.profile exists as well. - Simo
class UserProfileMixin(object):
    """
    This is a convenient mixin that set the user_profile object as a variable in the context
    so that it can be used in the template like this: {{ user_profile.user.email }}
    Moreover, it adds a reference to the same object in the class
    """

    def get_context_data(self, **kwargs):
        context = super(UserProfileMixin, self).get_context_data(**kwargs)
        context['user_profile'] = self.request.user.profile
        return context


class UserProfileDetailView(LoginRequiredMixin, UserProfileMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'user_profile_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        if self.request.user.profile.is_developer():
            context['games'] = Game.objects.filter(dev=self.request.user.profile)
        return context


class UserProfileUpdateView(LoginRequiredMixin, UserProfileMixin, UpdateView):
    form_class = UserUpdateModelForm
    login_url = reverse_lazy('login')
    model = User
    success_url = reverse_lazy('profile:user-profile')
    template_name = 'user_profile_update_view.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.get_form(self.form_class)
        user_profile_form = UserProfileUpdateModelFormset(
            queryset=UserProfile.objects.filter(user=self.get_object())
        )
        return self.render_to_response(self.get_context_data(user_form=user_form, user_profile_form=user_profile_form))

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.get_form(self.form_class)
        user_profile_form = UserProfileUpdateModelFormset(
            request.POST,
            request.FILES
        )
        if user_form.is_valid():
            user_form.save()
            user_profile_form.save(commit=False)
            """
            There is always one and only one formset (one user_profile for every user)
            hence we only and always save the first formset
            """
            user_profile_form[0].instance.user = self.get_object()
            user_profile_form[0].save()
            return super(UserProfileUpdateView, self).form_valid(form=user_form)
        else:
            return render(request, self.template_name, {'user_form': user_form, 'user_profile_form': user_profile_form})


"""
def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('profile:user-profile'))
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user:
                auth.login(request, user)
                user_profile = UserProfile.objects.get(user=user)
                request.session['user_profile_id'] = user_profile.id
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                messages.add_message(request, messages.ERROR, _('The entered credentials were regrettably incorrect.'))
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})


def registration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('home'))
    if request.method == 'GET':
        user_form = RegistrationUserModelForm()
        user_profile_form = RegistrationUserProfileModelForm()
        return render(request, 'registration.html', {'user_form': user_form, 'user_profile_form': user_profile_form})
    elif request.method == 'POST':
        user_form = RegistrationUserModelForm(request.POST, request.FILES)
        user_profile_form = RegistrationUserProfileModelForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user_profile_form.instance.user = user
            if user_profile_form.is_valid():
                user = User.objects.create_user(username=user.username,
                                                email=user.email,
                                                password=user.password,
                                                **{'first_name': user.first_name,
                                                   'last_name': user.last_name})
                user_profile_form.instance.user = user
                user_profile_form.instance.user_id = user.id
                user_profile_form.save()
                if user_profile_form.cleaned_data['user_type'] == RegistrationUserProfileModelForm.DEVELOPER_SLUG:
                    group = Group.objects.get(pk=1)
                    user.groups.set([group])
                    user.save()
                else:
                    group = Group.objects.get(pk=2)
                    user.groups.set([group])
                    user.save()
            return HttpResponseRedirect(reverse('profile:user-profile'))
        return render(request, 'registration.html', {'user_form': user_form, 'user_profile_form': user_profile_form})
"""

"""
class UserSignupView(FormView, ProcessFormView):
    template_name = 'signup.html'
    form_class = SignupPlayerForm
    
    def get(self, request, *args, **kwargs):
        # Don’t allow signups if the user is logged in
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('home'))
        return super(UserSignupView, self).get(self, request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = SignupPlayerForm(request.POST, request.FILES)
        #form_user = SignupUserForm(request.POST)
        #form_profile = SignupUserForm(request.POST, request.FILES)
        if form.is_valid():
            
            form.save()
            
            if 'is_developer' in form_profile.cleaned_data:
                group = Group.objects.get(pk=1)
            else:
                group = Group.objects.get(pk=2)
            user.groups.set([group])
            
            
            #user.save()
            #user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        
            return HttpResponseRedirect(reverse('profile:user-profile'))
        else:
            messages.add_message(request, messages.WARNING, form_user.errors)
            messages.add_message(request, messages.WARNING, form_profile.errors)
        return super(UserSignupView, self).get(self, request, *args, **kwargs)
"""
