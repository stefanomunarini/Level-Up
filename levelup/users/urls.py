"""levelup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django
from django.conf.urls import url
from django.contrib.auth.views import password_reset, logout
from django.urls import reverse_lazy

from users.views import UserProfileDetailView, UserProfileUpdateView, login, register

urlpatterns = [

    # Auth
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': reverse_lazy('profile:login')}, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^login/password_reset/$', password_reset, name='password_reset'),


    # Profile
    # url(r'^(?P<pk>[0-9]+)/$', UserProfileDetailView.as_view(), name='user-profile'),
    url(r'^$', UserProfileDetailView.as_view(), name='user-profile'),
    url(r'^update/$', UserProfileUpdateView.as_view(), name='user-profile-update'),
]
