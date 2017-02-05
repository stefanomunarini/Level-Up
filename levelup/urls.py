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
from django.contrib.auth.views import login

from api import urls as api_urls
from games import urls as games_url
from transactions import urls as transactions_url
from users import urls as users_url
from . import settings
from .views import HomepageView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include(users_url, namespace='profile')),
    url(r'^profile/', include('allauth.urls')),
    url(r'^games/', include(games_url, namespace='game')),
    url(r'^transactions/', include(transactions_url, namespace='transactions')),
    url(r'^$', HomepageView.as_view(), name='home'),
    
    # Auth
    url(r'^login/$', login, {'template_name': 'auth/login.html'}, name='login'),
    url('^', include('django.contrib.auth.urls')),
    
    # Set language
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # APIs v1
    url(r'^api/v1/', include(api_urls, namespace='api')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
