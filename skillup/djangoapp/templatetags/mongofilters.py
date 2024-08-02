from django import template
register = template.Library()

@register.filter(name='mongo_id')
def mongo_id(resource):
    return str(resource['_id'])

@register.filter(name='round')
def round_val(value):
    if value == '' or value is None:
        return 0 
    if type(value) != float:
        int(value)
    return round(value)