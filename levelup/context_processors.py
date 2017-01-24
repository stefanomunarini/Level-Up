from django.utils.translation import ugettext_lazy as _


def menu_structure(request):
    return {
        'main_menu': {
            'left': [
                {'label': _('Home'), 'view': 'home', 'icon': 'home'},
                {'label': _('My Games'), 'view': 'game:my-games', 'icon': 'gamepad',
                 'hide': not request.user.is_authenticated()},
                {'label': _('Store'), 'view': 'game:store', 'icon': 'shopping-basket'},
                {'label': _('Add Game'), 'view': 'game:add', 'icon': 'plus',
                 'hide': not request.user.is_authenticated() or not request.user.profile.is_developer},
                # {'label': _('Published Games'), 'view': 'game:my-games show_games_that_are="bought-by-the-user"', 'icon': 'gamepad',
                #  'hide': not request.user.is_authenticated() or not request.user.profile.is_developer},
            ],
            'right': [

            ],
        }
    }
