"""
This module provides functionality to insert data into a DuckDB database.
"""

import duckdb


def insert_data(row, table, conn):
    """Insert data into the specified table in the DuckDB database.

    Args:
        data (polars.DataFrame): DataFrame containing the data to be inserted into the database.
        table (str): The name of the table to insert data into.

    Returns:
        int: 404 if there is a constraint exception.
        None: If there is any other exception.
        bool: True if the data is inserted successfully.

    Raises:
        duckdb.ConstraintException: Raised when there is a constraint violation in the DuckDB database.
    """

    try:
        data_length = len(row)
        conn.execute(
            f'INSERT INTO {table} VALUES ({"?, " * (data_length - 1)}?)',
            row,
        )
    except duckdb.ConstraintException:
        return 404
    except duckdb.BinderException as e:
        print(f"Error inserting data: {e}")
        return 500