#!/usr/bin/env python3
"""
Pagination example
"""

from typing import Tuple


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
