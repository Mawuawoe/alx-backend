#!/usr/bin/python3
""" LFUCache class that implements a LFU caching system """
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache defines a LFU caching system
    """
    def __init__(self):
        super().__init__()
        self.frequency = {}  # Frequency of access for each key
        self.order = []      # Order of keys based on access
        self.min_freq = 0    # Track the minimum frequency of access

    def put(self, key, item):
        """
        Add an item in the cache
        """
        if key is None or item is None:
            return  # Do nothing if key or item is

        # If the item is new (not in cache)
        if key not in self.cache_data:
            # check and delete from cache if cache is full
            # before adding to cache
            self.discard_lfu()

            # put frequency to 1, add to order
            self.cache_data[key] = item
            self.frequency[key] = 1
            self.order.append(key)
            self.min_freq = 1

        else:
            # key already in cache, put update
            # increase frequency, change order
            self.cache_data[key] = item
            self.frequency[key] += 1
            self.order.remove(key)
            self.order.append(key)

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None  # Return None if the key is invalid

        # Update frequency and order when getting an item
        self.frequency[key] += 1
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]

    def discard_lfu(self):
        """Find the least frequently used items
        """
        min_freq_keys = \
            [k for k, v in self.frequency.items() if v == self.min_freq]

        if min_freq_keys:
            # We have multiple candidates, apply LRU to discard
            lru_key = min(min_freq_keys, key=lambda k: self.order.index(k))
            print("DISCARD:", lru_key)
            del self.cache_data[lru_key]
            del self.frequency[lru_key]
            self.order.remove(lru_key)

        # Update min_freq
        if not self.frequency:  # If frequency is empty, reset min_freq
            self.min_freq = 0
        else:
            self.min_freq = min(self.frequency.values())
