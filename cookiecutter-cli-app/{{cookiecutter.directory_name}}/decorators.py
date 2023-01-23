import functools
import logging
import time

logger = logging.getLogger(__name__)

def timer(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        start_time = time.perf_counter()
        
        output = func(*args, **kwargs)
        
        # Do something after
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.debug(f'Finished {func.__name__!r} in {run_time:.4f} secs.')
        return output
    return wrapper_decorator