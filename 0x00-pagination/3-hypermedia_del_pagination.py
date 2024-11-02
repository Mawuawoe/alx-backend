#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Return a dictionary with pagination data.
        """
        assert index is None or (0 <= index < len(self.indexed_dataset()))
        assert page_size > 0

        indexed_data = self.indexed_dataset()
        page_data = []
        current_index = index

        while len(page_data) < page_size and current_index < len(indexed_data):
            if current_index in indexed_data:
                page_data.append(indexed_data[current_index])
            current_index += 1

        if current_index < len(indexed_data):
            next_index = current_index
        else:
            next_index = None

        return {
            'index': index,
            'next_index': next_index,
            'page_size': len(page_data),
            'data': page_data
        }