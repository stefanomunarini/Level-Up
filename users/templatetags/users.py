from django import template

from users.forms import ApiKeyForm

register = template.Library()


@register.filter(name='get_class')
def get_class(value):
    # import ipdb;ipdb.set_trace();
    return value.__class__.__name__


@register.simple_tag()
def api_key_form():
    return ApiKeyForm().as_p()