#!/usr/bin/env python3
"""
Pagination example
"""
import csv
import math
from typing import List, Tuple, Dict, Any


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculates the start and end indices for paginating a dataset.

    Parameters:
    - page (int): The current page number (1-based).
    - page_size (int): The number of items per page.

    Returns:
    - Tuple[int, int]: A tuple containing the start index (inclusive)
      and end index (exclusive) for the items on the specified page.
      The start index is zero-based.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a page of data from the dataset.

        Parameters:
        - page (int): The current page number (1-based).
        - page_size (int): The number of items per page.

        Returns:
        - List[List]: A list of rows from the dataset for the specified page.
          If page or page_size is out of range, returns an empty list.
        """
        # Use assert to verify that both arguments
        # are integers greater than 0.
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        # Get the dataset for pagination
        all_data = self.dataset()

        # unpack start and end point
        start_index, end_index = index_range(page, page_size)

        if start_index >= len(all_data):
            return []

        paginated_data = all_data[start_index:end_index]
        return paginated_data

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Returns paginated data with hypermedia metadata.
        """
        # get the data per page
        page_data = self.get_page(page, page_size)

        total_items = len(self.dataset())
        total_pages = math.ceil(total_items / page_size)

        hypermedia = {
            "page_size": len(page_data),
            "page": page,
            "data": page_data,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages
        }
        return hypermedia
