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
    SignupUserGroupSelectionView, SignupPlayerView, SignupDeveloperView,
    UserProfileDetailView, UserProfileUpdateView, NewApiKeyView
)

urlpatterns = [
    
    # Profile
    url(r'^signup/$', SignupUserGroupSelectionView.as_view(), name='signup'),
    url(r'^signup/player$', SignupPlayerView.as_view(), name='signup-player'),
    url(r'^signup/developer$', SignupDeveloperView.as_view(), name='signup-developer'),
    url(r'^$', UserProfileDetailView.as_view(), name='user-profile'),
    url(r'^update/$', UserProfileUpdateView.as_view(), name='user-profile-update'),

    url(r'^create-api-key/$', NewApiKeyView.as_view(), name='create-api-key'),
    
]
