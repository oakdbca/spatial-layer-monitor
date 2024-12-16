"""Django Users Template Tag."""


# Third-Party
from django import template


# Register Template Tag
register = template.Library()

@register.filter
def is_authenticated_staff_or_superuser(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)
