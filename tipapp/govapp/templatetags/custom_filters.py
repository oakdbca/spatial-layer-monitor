import re
from django import template

register = template.Library()

@register.filter(name='add_newline_before_attribute')
def add_newline_before_attribute(value):
    if not isinstance(value, str):
        return value
    # return value.replace('Attribute', '<br>Attribute')
    value = re.sub(r'(?<!^)Attribute', '<br>Attribute', value)
    return value