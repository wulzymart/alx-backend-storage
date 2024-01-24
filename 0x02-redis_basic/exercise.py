#!/usr/bin/env python3
"""Create a Cache class. In the __init__ method,
store an instance of the Redis client as a private variable
named _redis (using redis.Redis())
and flush the instance using flushdb.
Create a store method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid),
store the input data in Redis using the random key and return the key.
"""

from redis import Redis
from uuid import uuid4
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def fn(self, *args, **kwargs) -> Any:
        '''calls the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return fn


def call_history(method: Callable) -> Callable:
    '''records imput and output hx of methods.
    '''
    @wraps(method)
    def fn(self, *args, **kwargs) -> Any:
        '''stores imput and output of a method and returns its value
        '''
        input_key = f'{method.__qualname__}:inputs'
        output_key = f'{method.__qualname__}:outputs'
        if isinstance(self._redis, Redis):
            self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        if isinstance(self._redis, Redis):
            self._redis.rpush(output_key, result)
        return result
    return fn


def replay(fn: Callable):
    """replays function hx"""
    print(fn.__self__)
    if not fn or not hasattr(fn, '__self__')\
            or not isinstance(fn.__self__, Cache):
        return
    cache = fn.__self__
    name = fn.__qualname__
    call_count = cache.get(name, int) or 0
    print(f'{name} was called {call_count} times:')
    redis_inst = getattr(cache, "_redis")
    input_key = f'{name}:inputs'
    output_key = f'{name}:outputs'
    inputs = redis_inst.lrange(input_key, 0, -1)
    outputs = redis_inst.lrange(output_key, 0, -1)
    for input, output in zip(inputs, outputs):
        print(f'{name}(*{input.decode("utf-8")}) -> {output}')


class Cache:
    """class of redis cache"""
    def __init__(self):
        """initialise the cache"""
        self._redis = Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, int, float, bytes]) -> str:
        """stores a data in the catch"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Union[Callable, None] = None) ->\
            Union[str, bytes, int, float]:
        """gets an item from cache and processes it"""
        data = self._redis.get(key)
        if fn:
            return fn(data) if data else None
        else:
            return data
