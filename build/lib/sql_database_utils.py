
"""
This module contains several utility functions for reading data from SQL Server Databases.

The module contains the following functions:

- read_table → Reads an entire table into a DataFrame.
- read_with_filter → Reads table with a WHERE clause (dynamic condition).
- delete_with_filter → Deletes table rows with a WHERE clause (dynamic condition).
- insert_dataframe:
    - Pulls the DB table schema first.
    - Checks if the DataFrame has any extra columns → stops with an error.
    - Missing columns are auto-filled with NULL (Python None).
    - Generates a parameterized insert query to avoid SQL injection.
    - Inserts row-by-row (safe for small/medium inserts; for large batches, we can optimize to bulk insert).
"""


import pyodbc
import pandas as pd

def read_table(table_name: str, conn_str: str) -> pd.DataFrame:
    """
    Reads an entire table from SQL Server into a pandas DataFrame.
    
    Args:
        table_name (str): Name of the table to read.
        conn_str (str): ODBC connection string.
    
    Returns:
        pd.DataFrame: DataFrame containing table data.

    Examples
    --------
    >>> conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=server;DATABASE=db;UID=user;PWD=password"
    >>> df = read_table("Customers", conn_str)
    >>> print(df.head())
    """
    with pyodbc.connect(conn_str) as conn:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
    return df


def read_with_filter(table_name: str, conn_str: str, column_name: str, condition: str) -> pd.DataFrame:
    """
    Reads a filtered set of rows from a table using a WHERE clause.
    
    Args:
        table_name (str): Name of the table to read.
        conn_str (str): ODBC connection string.
        column_name (str): Column name for the filter.
        condition (str): SQL condition (e.g., "= 'value'", "> 10").
    
    Returns:
        pd.DataFrame: DataFrame containing filtered table data.

    Examples
    --------
    >>> conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=server;DATABASE=db;UID=user;PWD=password"
    >>> df = read_table_with_filter("Orders", conn_str, "OrderAmount", "> 500")
    >>> print(df.head())

    >>> df = read_table_with_filter("Employees", conn_str, "Country", "= 'USA'")
    >>> print(df)
    """
    with pyodbc.connect(conn_str) as conn:
        query = f"SELECT * FROM {table_name} WHERE {column_name} {condition}"
        df = pd.read_sql(query, conn)
    return df


def delete_with_filter(table_name: str, conn_str: str, column_name: str, condition: str) -> int:
    """
    Deletes rows from a SQL Server table based on a WHERE condition.
    
    Args:
        table_name (str): Name of the table to delete rows from.
        conn_str (str): ODBC connection string.
        column_name (str): Column name for the filter.
        condition (str): SQL condition (e.g., "= 'value'", "> 10").
    
    Returns:
        int: Number of rows deleted.
    """
    rows_deleted = 0
    try:
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                # Build the SQL DELETE statement dynamically but safely
                query = f"DELETE FROM {table_name} WHERE {column_name} {condition};"
                
                print(f"Executing: {query}")
                cursor.execute(query)
                rows_deleted = cursor.rowcount

                # Commit transaction
                conn.commit()

                print(f"{rows_deleted} rows deleted from {table_name}.")
    except pyodbc.Error as e:
        print("❌ Database error occurred:", e)
    except Exception as ex:
        print("⚠️ Unexpected error:", ex)

    return rows_deleted



def insert_dataframe(table_name: str, conn_str: str, df: pd.DataFrame):
    """
    Inserts a pandas DataFrame into a SQL Server table after schema validation.
    
    Args:
        table_name (str): Name of the table to insert into.
        conn_str (str): ODBC connection string.
        df (pd.DataFrame): DataFrame to insert. Columns must match DB table schema.
    
    Raises:
        ValueError: If DataFrame has columns not found in DB table schema.

    Examples
    --------
    >>> conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=server;DATABASE=db;UID=user;PWD=password"
    >>> data = {"CustomerID": [1, 2], "CustomerName": ["Alice", "Bob"]}
    >>> df = pd.DataFrame(data)
    >>> insert_dataframe("Customers", conn_str, df)
    """
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()

        # Fetch table schema
        cursor.execute(f"SELECT TOP 0 * FROM {table_name}")
        table_columns = [column[0] for column in cursor.description]

        # Check for extra columns in DataFrame
        extra_columns = set(df.columns) - set(table_columns)
        if extra_columns:
            raise ValueError(f"DataFrame contains columns not in table: {extra_columns}")

        # Align DataFrame columns with table schema, filling missing with None
        insert_columns = table_columns[:len(table_columns)]
        aligned_df = pd.DataFrame(columns=insert_columns)
        for col in insert_columns:
            aligned_df[col] = df[col] if col in df.columns else None

        # Prepare parameterized INSERT query
        placeholders = ", ".join(["?"] * len(insert_columns))
        columns_str = ", ".join(insert_columns)
        insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

        # Insert each row
        for row in aligned_df.itertuples(index=False, name=None):
            cursor.execute(insert_sql, row)

        conn.commit()
        print(f"Inserted {len(aligned_df)} rows into {table_name}")
