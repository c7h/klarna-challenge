import sys
import os
import math
import logging
import functools

log = logging.getLogger(__name__)

# get config from env
recursionlimit = int(os.environ.get('RECURSION_LIMIT', 2000))
sys.setrecursionlimit(recursionlimit)  # For demo purpose
log.debug("Recursion Limit set to {}".format(recursionlimit))


@functools.lru_cache(None)
def fib_simple(n):
    """
    Simple, itterative version of the fibonacci fuction.
    Since, it's a deterministic function, we can cache the
    result with the lru_cache.
    This has some major drawbacks for web services:
    1. Sideeffects, which destroy the idempotent characters of the endpoint.
       with a clear cache, the function can run up to the recursion limit and fill the cache.
       The second function call can run to a number almost twice as big as the first number,
       since in uses the cached values. This sounds awesome, but violates concepts of REST.
    2. If the cache it lost, the process restarts and might not give results wich depend on
       cache lookups.
    :param n: integer (this awesome function also handles negative ones)
    """
    if n <= -1:
        return int(((-1)**(n+1)) * fib_simple(-n))
    if n < 2:
        return n
    return fib_simple(n-1) + fib_simple(n-2)


@functools.lru_cache(None)
def ackermann_simple(m, n):
    if m == 0:
        return n+1
    if n == 0:
        return ackermann_simple(m-1, 1)
    try:
        n2 = ackermann_simple(m, n-1)
    except RecursionError as e:
        log.warning(e)
        raise e
    return ackermann_simple(m-1, n2)


def ackermann_redis(m, n, redis_instance=None):
    """
    Ackermann function using a redis cache.
    This has the advantage, that previously calculated 
    (sub)steps can be retrieved from the cache. This saves
    calculation time.
    """
    r = redis_instance
    b = r.hget(m, n)
    if b:
        return int(b)
    else:
        if m == 0:
            result = n+1
        if m == 1:
            result = n+2
        elif n == 0:
            result = ackermann_redis(m-1, 1, r)
        else:
            # may raise recursion error:
            n2 = ackermann_redis(m, n-1, r)
            result = ackermann_redis(
                    m-1,
                    n2,
                    r)
        r.hsetnx(m, n, result)
        return result


def ackermann_wolfram(m, n, wolfram_id):
    """
    Ackermann as a Service.
    It might look tempting to add theses results to the redis cache of
    `ackermann_redis`, but opens the door for potential cache poisoning if
    the third-party service gets compromised.
    NOTE: We could return the fuction value in arrow notation if the value is too big to display
    """
    import wolframalpha
    client = wolframalpha.Client(wolfram_id)
    res = client.query("ackermann({}, {})".format(m, n))
    # filter result
    result_pod = filter(lambda x: x.get('@title') == 'Result', res)
    property_pod = filter(lambda x: x.get('@title') == 'Argument tally', res)

    try:
        # get statistics
        rl = list(property_pod).pop()
        recursion_count = rl['subpod'][0]['plaintext']
    except (KeyError, IndexError):
        log.warning("Could not get meta information from wolframalpha")

    # get result
    try:
        rl = list(result_pod).pop()  # Should always have a result
        result = rl['subpod']['plaintext']
    except (KeyError, IndexError):
        raise RuntimeError("Could not fetch result from server")
    if "too large to represent" in result:
        raise RecursionError("Computation too complicated")

    return int(result)


@functools.lru_cache(None)
def factorial(x):
    return math.factorial(x)
