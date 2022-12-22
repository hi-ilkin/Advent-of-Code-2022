from functools import wraps
import time


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t = time.time()
        result = func(*args, **kwargs)
        print(f"function {func.__name__} took {(time.time() - t)*1000:.3f} ms.")
        return result

    return wrapper
