class Stopped(BaseException):
    """Raised inside a Decoratee to signal a `set_stopped` completion.

    Not a Decorator like the other entries in this package — Stopped is a
    plain exception type so it can flow through `try/except` chains and be
    caught at the algorithm boundary (e.g. `Just`, `Then`) without going
    through the decorator pipeline.
    """
