from django import template
register = template.Library()

@register.filter(name='mongo_id')
def mongo_id(resource):
    return str(resource['_id'])