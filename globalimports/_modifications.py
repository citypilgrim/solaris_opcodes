import functools

print = functools.partial(print, flush=True)
