from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter
def get_choice_display(obj, field_name):
    """
    Returns the display value for a choice field
    Usage: {{ object|get_choice_display:"field_name" }}
    """
    choices = {
        'N': 'Nunca',
        'P': 'Pasado',
        'A': 'Presente'
    }
    value = getattr(obj, field_name, '')
    return choices.get(value, value)

@register.filter(is_safe=True)
def json_script(value, element_id):
    """
    Convierte un valor a JSON y lo escapa apropiadamente
    """
    json_str = json.dumps(value, cls=DjangoJSONEncoder)
    return mark_safe(json_str)