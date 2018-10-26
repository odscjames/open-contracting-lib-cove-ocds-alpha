from functools import wraps  # use this to preserve function signatures and docstrings
from decimal import Decimal


def ignore_errors(f):
    @wraps(f)
    def ignore(json_data, *args, ignore_errors=False, return_on_error={}, **kwargs):
        if ignore_errors:
            try:
                return f(json_data, *args, **kwargs)
            except (KeyError, TypeError, IndexError, AttributeError, ValueError):
                return return_on_error
        else:
            return f(json_data, *args, **kwargs)
    return ignore


# From http://bugs.python.org/issue16535
class NumberStr(float):
    def __init__(self, o):
        # We don't call the parent here, since we're deliberately altering it's functionality
        # pylint: disable=W0231
        self.o = o

    def __repr__(self):
        return str(self.o)

    # This is needed for this trick to work in python 3.4
    def __float__(self):
        return self


def decimal_default(o):
    if isinstance(o, Decimal):
        if int(o) == o:
            return int(o)
        else:
            return NumberStr(o)
    raise TypeError(repr(o) + " is not JSON serializable")
