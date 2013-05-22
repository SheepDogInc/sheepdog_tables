from django import template
from django.core.urlresolvers import reverse

register = template.Library()


class CallNode(template.Node):
    """
    Call method of an object passing it args.  Also accepts an as parameter to set
    context variable.

    Basic usage:

    ::

        {% call obj callable arg1 arg2 arg3 arg4 as url %}

    As clause and args are totally optional

    :param obj: The object to take into context for the call.
    :param callable: The function we are going to call wrt the object.
    :param args: Any arguments that should be passed along.
    :param var: The variable in which to store the result.
    """
    def __init__(self, obj, callable, args, var):
        self.obj = obj
        self.callable = callable
        self.args = args
        self.var = var

    def render(self, context):
        """
        Render's the value, calling the function

        :param context: The current template context
        :return: Either the called result or ""
        """
        try:
            obj = context.get(self.obj, None)

            args = [context.get(arg, arg) for arg in self.args]
            result = getattr(obj, self.callable)(*args)

            if self.var:
                context[self.var] = result

            return result

        except template.VariableDoesNotExist:
            return ""

def call(parser, token):
    """
    Tag entry point.

    :param parser: Utility reasons.
    :param token: The string to split into a call.
    """
    try:
        contents = token.split_contents()

        tag_name = contents[0]
        obj = contents[1]
        callable = contents[2]
        args = contents[3:] or []

        # Chop off as if it exists
        if 'as' in args:
            args = args[:len(args) - 2]

        var_index = contents.index('as') if 'as' in contents else None
        var = contents[var_index + 1] if var_index is not None else None

    except ValueError:
        raise template.TemplateSyntaxError('%s requires at least 3 arguments' % tag_name)
    return CallNode(obj, callable, args, var)

register.tag('call', call)
