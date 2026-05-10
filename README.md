# sql_server_database_utils

Contains several python utility functions for reading data from SQL Server Databases. Lightweight functions optimized for pandas.

Uses ODBC Driver 17 for SQL Server and pyodbc module.

`sql_database_utils.py` contains the following functions:

- read_table → Reads an entire table into a DataFrame.
- read_with_filter → Reads table with a WHERE clause (dynamic condition).
- delete_with_filter → Deletes table rows with a WHERE clause (dynamic condition).
- insert_dataframe:
    - Pulls the DB table schema first.
    - Checks if the DataFrame has any extra columns → stops with an error.
    - Missing columns are auto-filled with NULL (Python None).
    - Generates a parameterized insert query to avoid SQL injection.
    - Inserts row-by-row (safe for small/medium inserts; for large batches, we can optimize to bulk insert).

## Download the latest release
```
pip install https://github.com/yxuan1996/sql_server_database_utils/releases/download/Production/sql_database_utils-0.2.0-py3-none-any.whl
```

## View Documentation
[Documentation](https://yxuan1996.github.io/sql_server_database_utils/)

## Building the wheel
`setup.py` contains instructions on how to package the module.

Run the 2 commands to build the wheel:
```
python setup.py clean --all
python setup.py bdist_wheel
```

Our python wheel file is now located in the `/dist` folder. 