from functools import wraps, partial

def partializable(*partial_params):
    def decorator(func):
        @wraps(func)
        def wrapper(**fixed_kwargs):
            if not all(k in partial_params for k in fixed_kwargs):
                raise ValueError(f"Only {partial_params} can be partialized")
            
            return partial(func, **fixed_kwargs)
        return wrapper
    return decorator