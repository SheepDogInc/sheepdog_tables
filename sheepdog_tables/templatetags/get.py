from django import template

register = template.Library()

def get(value, arg):
    try:
        return value[arg]
    except KeyError:
        return None

register.filter('get', get)

