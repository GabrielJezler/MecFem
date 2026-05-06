from functools import wraps, partial

def partializable(*partial_params):
    """
    Decorator to create a partial function with fixed keyword arguments.

    Example
    -------

    >>> @partializable('a', 'b')
    ... def my_function(a, b, c):
    ...     return a + b + c
    >>> my_partial = my_function(a=1, b=2)
    >>> my_partial(c=3)
    6
    """
    def decorator(func):
        @wraps(func)
        def wrapper(**fixed_kwargs):
            if not all(k in partial_params for k in fixed_kwargs):
                raise ValueError(f"Only {partial_params} can be partialized")
            
            return partial(func, **fixed_kwargs)
        return wrapper
    return decorator