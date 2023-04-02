from django import template
register = template.Library()

@register.filter
def at_index(array, index):
    return array[index]