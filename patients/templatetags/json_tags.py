from django import template
from django.core.serializers.json import DjangoJSONEncoder
import json

register = template.Library()

@register.filter
def json_script(value, element_id):
    """
    Convierte un valor a JSON y lo envuelve en una etiqueta script
    """
    json_str = json.dumps(value, cls=DjangoJSONEncoder)
    return f'<script id="{element_id}" type="application/json">{json_str}</script>'