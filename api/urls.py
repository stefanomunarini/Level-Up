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

from api.views import ApiDevelopedGamesView, ApiSaleStatsView, ApiGameStatsView, ApiGameSearchView, ApiTopGamesView

urlpatterns = [

    url(r'^developed-games/$', ApiDevelopedGamesView.as_view(), name='developed-games'),
    url(r'^sales-stats/$', ApiSaleStatsView.as_view(), name='sales-stats'),
    url(r'^game-stats/(?P<slug>[-\w]+)/$', ApiGameStatsView.as_view(), name='game-stats'),
    url(r'^game-search/$', ApiGameSearchView.as_view(), name='game-search'),
    url(r'^top-games/$', ApiTopGamesView.as_view(), name='top-games'),
    
]
