#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
from typing import Union, Optional, Callable, Any
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    decorator that takes a single method Callable
    argument and returns a Callable.
    """
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    decorator to store the history of inputs and
    outputs for a particular function
    """
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper


class Cache:
    """
    Create a Cache class.
    """

    def __init__(self) -> None:
        """
        store an instance of the Redis
        client as a private variable
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        method that takes a data argument and returns a string
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        method that take a key string argument and
        an optional Callable argument named fn
        """
        client = self._redis
        value = client.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value

    def get_str(self, date: bytes) -> str:
        """"convert bytes to string"""
        return date.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """convert bytes to intger"""
        return int(data)


def replay(method: Callable):
    """ display the history of calls of a particular function """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"
    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")
    print("{} was called {} times:".format(key, count))
    inputList = redis.lrange(inputs, 0, -1)
    outputList = redis.lrange(outputs, 0, -1)
    redis_zipped = list(zip(inputList, outputList))
    for a, b in redis_zipped:
        attr, data = a.decode("utf-8"), b.decode("utf-8")
        print("{}(*{}) -> {}".format(key, attr, data))
