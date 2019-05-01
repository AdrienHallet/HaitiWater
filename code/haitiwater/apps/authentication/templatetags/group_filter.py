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
    group = Group.objects.filter(user=user).first()
    if group is None:
        return ""
    return group.name


@register.filter(name='get_zone')
def get_zone(user):
    return user.profile.zone.name
