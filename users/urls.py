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
from django.conf.urls import url

from users.views import (
    SignupPlayerView, SignupDeveloperView,
    UserProfileDetailView, UserProfileUpdateView,
)

urlpatterns = [
    
    # Profile
    url(r'^signup/$', SignupPlayerView.as_view(), name='registration'),
    url(r'^signup/dev$', SignupDeveloperView.as_view(), name='registration-dev'),
    url(r'^$', UserProfileDetailView.as_view(), name='user-profile'),
    url(r'^update/$', UserProfileUpdateView.as_view(), name='user-profile-update'),
    
]
