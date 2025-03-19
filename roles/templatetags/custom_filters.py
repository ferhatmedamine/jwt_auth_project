from django import template

register = template.Library()

@register.filter
def has_role(user, role):
    """
    Custom template filter to check if a user has a specific role.
    Usage: {% if user|has_role:"org_admin" %}
    """
    return user.profile.role == role