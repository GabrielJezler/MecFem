import functools


def cache_none(func):
    cached_value = None
    has_cache = False

    @functools.wraps(func)
    def wrapper(arg, *args, **kwargs):
        nonlocal cached_value, has_cache

        if arg is None:
            if not has_cache:
                cached_value = func(arg, *args, **kwargs)
                has_cache = True
            return cached_value

        return func(arg, *args, **kwargs)

    return wrapper
