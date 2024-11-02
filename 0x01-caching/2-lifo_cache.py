#!/usr/bin/env python3
"""
LIFOCache module
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    FIFOCache defines a FIFO caching system
    """
    def __init__(self):
        """ Initialize the class """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        Add an item in the cache
        """
        if key is not None and item is not None:
            # If key already exists,
            # update the value and do not change order
            if key in self.cache_data:
                self.cache_data[key] = item
            # If adding a new item
            else:
                # and the cache exceeds MAX_ITEMS, discard last item
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    last_key = self.order.pop()
                    del self.cache_data[last_key]
                    print(f"DISCARD: {last_key}")

                # Add the new item to cache and keep track of its order
                self.cache_data[key] = item
                self.order.append(key)

    def get(self, key):
        """
        Get an item by key
        """
        return self.cache_data.get(key, None)
