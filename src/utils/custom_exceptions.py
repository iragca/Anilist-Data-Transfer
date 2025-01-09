"""
Module for custom exceptions used in the application.
"""

class NoAnimeEntriesFound(Exception):
    """
    Exception raised when no anime entries are found.
    """
    def __init__(self, message="No anime entries found"):
        self.message = message
        super().__init__(self.message)

class NoDataFound(Exception):
    """
    Exception raised when no data is found.
    """
    def __init__(self, message="No data found"):
        self.message = message
        super().__init__(self.message)

class RowInsertionError(Exception):
    """
    Exception raised when an error occurs during row insertion.
    """
    def __init__(self, message="Error inserting row"):
        self.message = message
        super().__init__(self.message)