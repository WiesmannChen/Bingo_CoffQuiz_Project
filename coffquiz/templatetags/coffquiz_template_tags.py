from django import template
from coffquiz.models import Coffee

register = template.Library()

@register.inclusion_tag('coffquiz/coffeelist.html')
def get_coffee_list(current_coffee=None):
    return {'coffeelist': Coffee.objects.all().order_by('-likes'), 'current_coffee': current_coffee}