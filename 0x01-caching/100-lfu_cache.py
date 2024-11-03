#!/usr/bin/python3
""" LFUCache class that implements a LFU caching system """
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache defines a LFU caching system
    """
    def __init__(self):
        super().__init__()
        self.frequency = {}  # Dictionary to track the frequency of each key
        # List to maintain the order of keys based on access
        self.order = []
        self.min_freq = 0    # Track the minimum frequency of access

    def put(self, key, item):
        """
        Add an item in the cache
        """
        if key is None or item is None:
            return  # Do nothing if key or item is None

        # If the item is new (not in cache)
        if key not in self.cache_data:
            # Check and delete from cache if it's full before adding to cache
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                self.discard_lfu()

            # Add new item to cache and set frequency to 1
            self.cache_data[key] = item
            self.frequency[key] = 1
            self.order.append(key)
            # Update min_freq to 1 since this is the first item
            self.min_freq = 1

        else:
            # Key already in cache, update the item and its frequency
            self.cache_data[key] = item
            self.frequency[key] += 1
            self.order.remove(key)  # Remove key from current position
            self.order.append(key)   # Append it to mark as recently used

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None  # Return None if the key is invalid

        # Update frequency and order when getting an item
        self.frequency[key] += 1
        self.order.remove(key)  # Remove key from current position
        self.order.append(key)   # Append it to mark as recently used
        return self.cache_data[key]

    def discard_lfu(self):
        """Find and discard the least frequently used item."""
        min_freq_keys = \
            [k for k, v in self.frequency.items() if v == self.min_freq]

        if min_freq_keys:
            # If there are multiple candidates, apply LRU to discard
            lru_key = min(min_freq_keys, key=lambda k: self.order.index(k))
            print("DISCARD:", lru_key)
            del self.cache_data[lru_key]  # Remove from cache
            del self.frequency[lru_key]     # Remove frequency tracking
            self.order.remove(lru_key)      # Remove from order tracking

        # Update min_freq
        if not self.frequency:  # If frequency is empty, reset min_freq
            self.min_freq = 0
        else:
            # Update min_freq based on remaining items
            self.min_freq = min(self.frequency.values())
