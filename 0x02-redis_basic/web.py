#!/usr/bin/env python3
"""Implementing an expiring web cache and tracke"""
import redis
from requests import get

client = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """
    The core of the function is very simple.
    It uses the requests module to obtain the
    HTML content of a particular URL and returns it.
    """
    client.set(f"cached:{url}", count)
    client.incr(f"count:{url}")
    request = get(url)
    client.setex(f"cached:{url}", 10, client.get(f"cached:{url}"))

    return request.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
