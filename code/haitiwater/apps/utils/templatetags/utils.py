from django import template

register = template.Library()


@register.filter(name='range_from_one')
def range_from_one(number):
    return range(1, number)
