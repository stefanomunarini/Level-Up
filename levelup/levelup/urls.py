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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.i18n import set_language

from foundation import urls as foundation_urls

from users import urls as users_url
from games import urls as games_url
from users.views import home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include(users_url, namespace='profile')),
    url(r'^game/', include(games_url, namespace='game')),
    url(r'^$', home, name='home'),
    
    # Set language
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
