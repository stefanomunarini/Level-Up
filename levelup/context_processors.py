from django.utils.translation import ugettext_lazy as _


def menu_structure(request):
    return {
        'main_menu': {
            'left': [
                {'label':_('Home'), 'view':'home', 'icon':'home'},
                {'label':_('My Games'), 'view': 'game:my-games', 'icon': 'gamepad', 'hide': not request.user.is_authenticated()},
                {'label':_('Store'), 'view': 'game:store', 'icon': 'shopping-basket'},
            ],
            'right': [

            ],
        }
    }