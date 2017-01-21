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
from django.utils.translation import ugettext_lazy as _

from games.views import (
    GameDetailView, GameListView, GamePlayView, GameStateView,
    GameBuyView, GameCreateView, GameDeleteView, GameUpdateView,
)

urlpatterns = [
    url(r'^$', GameListView.as_view(bought=True, page_title=_('My Games')), name='my-games'),
    url(r'^store/$', GameListView.as_view(page_title=_('Store')), name='store'),
    url(r'^add/$', GameCreateView.as_view(), name='add'),
    url(r'^(?P<slug>[-\w]+)/$', GameDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[-\w]+)/play$', GamePlayView.as_view(), name='play'),
    url(r'^(?P<slug>[-\w]+)/buy$', GameBuyView.as_view(), name='buy'),
    url(r'^(?P<slug>[-\w]+)/update$', GameUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>[0-9]+)/delete$', GameDeleteView.as_view(), name='delete'),
    url(r'^(?P<slug>[-\w]+)/buy$', GameStateView.as_view(), name='game-state'),
]
