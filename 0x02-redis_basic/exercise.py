#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
from typing import Union, Optional, Callable, Any
from uuid import uuid4


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
