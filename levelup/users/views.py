from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from users.models import UserProfile
from users.forms import LoginForm, UserModelForm, UserProfileModelForm, UserUpdateModelForm, UserProfileUpdateModelForm


class UserProfileMixin(object):
    """
    This is a convenient mixin that set the user_profile object as a variable in the context
    so that it can be used in the template like this: {{ user_profile.user.email }}
    """
    def get_context_data(self, **kwargs):
        context = super(UserProfileMixin, self).get_context_data(**kwargs)
        context['user_profile'] = get_object_or_404(UserProfile, id=self.request.session.get('user_profile_id'))
        return context


class UserProfileDetailView(LoginRequiredMixin, UserProfileMixin, TemplateView):
    login_url = reverse_lazy('profile:login')
    template_name = 'user_profile_detail_view.html'


class UserProfileUpdateView(LoginRequiredMixin, UserProfileMixin, UpdateView):
    form_class = UserUpdateModelForm
    model = User
    success_url = reverse_lazy('profile:user-profile')
    template_name = 'user_profile_update_view.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.get_form(self.form_class)
        user_profile_form = UserProfileUpdateModelForm(
            initial=model_to_dict(UserProfile.objects.get(user=self.get_object())))
        return self.render_to_response(self.get_context_data(user_form=user_form, user_profile_form=user_profile_form))

    def get_object(self, queryset=None):
        self.object = User.objects.get(userprofile__id=self.request.session.get('user_profile_id'))
        return self.object

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.get_form(self.form_class)
        user_profile_form = UserProfileUpdateModelForm(
            request.POST,
            request.FILES
        )
        import ipdb; ipdb.set_trace()
        if user_form.is_valid() & user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return HttpResponseRedirect(reverse_lazy('profile:user-profile'))
        else:
            return render(request, self.template_name, {'user_form': user_form, 'user_profile_form': user_profile_form})


def login(request):
    if request.method == 'GET':
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
                return HttpResponseRedirect(reverse('profile:user-profile'))
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Incorrect credentials!'})
        else:
            return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'GET':
        user_form = UserModelForm()
        user_profile_form = UserProfileModelForm()
        return render(request, 'register.html', {'user_form': user_form, 'user_profile_form': user_profile_form})
    elif request.method == 'POST':
        user_form = UserModelForm(request.POST, request.FILES)
        user_profile_form = UserProfileModelForm(request.POST)
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
                if user_profile_form.cleaned_data['user_type'] == UserProfileModelForm.DEVELOPER_SLUG:
                    group = Group.objects.get(pk=1)
                    user.groups.set([group])
                    user.save()
                else:
                    group = Group.objects.get(pk=2)
                    user.groups.set([group])
                    user.save()
            return HttpResponseRedirect(reverse('profile:login'))
        return render(request, 'register.html', {'user_form': user_form, 'user_profile_form': user_profile_form})
