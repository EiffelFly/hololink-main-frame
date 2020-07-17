from django import template
register = template.Library()

@register.filter
def indexforloop(indexable, i):
    return indexable[i]