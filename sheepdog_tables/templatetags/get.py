from django import template

register = template.Library()

def get(value, arg):
    """
    Get item from dict or list

    :param value: The dict like object we are grabbing from
    :param arg: The index or key we are accessing
    :return: The found value or none.
    """
    try:
        return value[arg]
    except KeyError:
        return None

register.filter('get', get)

