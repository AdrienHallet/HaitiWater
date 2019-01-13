from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False
    return group in user.groups.all()

@register.filter(name='get_group')
def get_group(user):
    query_set = Group.objects.filter(user=user)
    if len(query_set) == 1:
        user_group = query_set[0].name
        return user_group
    else:
        return ""

@register.filter(name='get_zone')
def get_zone(user):
    return user.profile.zone.name