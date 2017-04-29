from functools import lru_cache
from functools import wraps


class _DoNotCache(Exception):
    pass


def _intercept(exception_type, return_value=None):
    def intercept_wrapper(func):
        @wraps(func)
        def interceptor(*func_args, **func_kwargs):
            try:
                return func(*func_args, **func_kwargs)
            except exception_type as ex:
                return getattr(ex, '_return_value', return_value)
        return interceptor
    return intercept_wrapper


def _raise_if_falsy(exception_type):
    def raise_if_falsy_wrapper(func):
        @wraps(func)
        def raises_if_falsy(*func_args, **func_kwargs):
            return_value = func(*func_args, **func_kwargs)
            if not return_value:
                ex = exception_type()
                setattr(ex, '_return_value', return_value)
                raise ex
            return return_value
        return raises_if_falsy
    return raise_if_falsy_wrapper


def lru_cache_truthy_only(*lru_cache_args, **lru_cache_kwargs):
    def lru_cache_truthy_only_wrapper(func):
        @wraps(func)
        @lru_cache(*lru_cache_args, **lru_cache_kwargs)
        @_raise_if_falsy(_DoNotCache)
        def caches_if_truthy(*func_args, **func_kwargs):
            return func(*func_args, **func_kwargs)

        wrapped = _intercept(_DoNotCache)(caches_if_truthy)
        wrapped.cache_info = caches_if_truthy.cache_info
        return wrapped

    return lru_cache_truthy_only_wrapper
