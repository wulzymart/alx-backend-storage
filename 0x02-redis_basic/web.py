#!/usr/bin/env python3
"""caches a websites result"""


from redis import Redis
import requests
from functools import wraps
from typing import Callable


def cache(function: Callable) -> Callable:
    """Decorator for cacing"""

    @wraps(function)
    def fn(url):
        """caches a url"""
        redis = Redis()
        count_key = f"count:{url}"
        result_key = f"result:{url}"
        print

        result = redis.get(result_key)
        if result:
            redis.incr(count_key)
            return result
        redis.set(count_key, 0)
        result = function(url)
        redis.setex(result_key, 10, result)
        return result
    return fn


@cache
def get_page(url: str) -> str:
    """gets a url through requests"""
    resp = requests.get(url)
    return resp.text
