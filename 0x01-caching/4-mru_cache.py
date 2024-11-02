#!/usr/bin/env python3
"""
MRUCache module
"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache defines a LRU caching system
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
            # update the value and change order
            # any time you try to put item to cache,
            # it is most recently used
            # move it to the back
            if key in self.cache_data:
                self.cache_data[key] = item
                self.order.remove(key)
                self.order.append(key)
            # If adding a new item
            else:
                # and the cache exceeds MAX_ITEMS, discard last item
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    mru_key = self.order.pop()
                    del self.cache_data[mru_key]
                    print(f"DISCARD: {mru_key}")

                # Add the new item to cache and keep track of its order
                self.cache_data[key] = item
                self.order.append(key)

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None

        # Move the accessed key to the end to mark it as recently used
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
