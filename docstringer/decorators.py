import functools

from .events import FunctionEvent
from .formatters import BaseFormatter, DefaultFormatter


def docstringer(
    _func=None, *, active=True, formatter: BaseFormatter = DefaultFormatter()
):
    """ 
    A decorator that will output the function docstring, call values and return value when the function is called.
    Add this decorator to all functions you want to have documented this way.

    Parameters:
    - active (bool) default=True - this controls if the docstringer is active
    - formatter (Formatter instance) - this allows docstringer to output the results in a different format or data structure
    """

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):

            if not active:
                return func(*args, **kwargs)

            event = FunctionEvent(func, *args, **kwargs)
            formatter.call(event)

            return_value = func(*args, **kwargs)

            event.return_value = return_value
            formatter.end(event)

            return return_value

        return inner

    if _func is None:
        return wrapper
    else:
        return wrapper(_func)

