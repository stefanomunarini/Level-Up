from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from users.models import UserProfile
from users.forms import LoginForm, UserModelForm, UserProfileModelForm


class UserProfileDetailView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('profile:login')
    template_name = 'user_profile_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context['user_profile'] = get_object_or_404(UserProfile, id=self.request.session.get('user_profile_id'))
        return context


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
        user_form = UserModelForm(request.POST)
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
            return HttpResponseRedirect(reverse('profile:login'))
        return render(request, 'register.html', {'user_form': user_form, 'user_profile_form': user_profile_form})
