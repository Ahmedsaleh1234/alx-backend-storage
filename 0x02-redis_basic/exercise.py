#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
from typing import Union
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
