# SQL Database Utils

A lightweight Python utility module for reading, writing, and manipulating data from SQL Server Databases. Optimized for use with pandas DataFrames.

## Features

- **Read entire tables** into pandas DataFrames
- **Filtered reads** using dynamic WHERE clauses
- **Row deletion** with WHERE conditions
- **Safe data insertion** with parameterized queries (SQL injection protection)
- **Schema validation** for DataFrame inserts
- **ODBC Driver 17** for SQL Server support

## Quick Start

```python
import sql_database_utils as db

# Connection string
conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=server;DATABASE=db;UID=user;PWD=password"

# Read an entire table
df = db.read_table("Customers", conn_str)

# Read with filter
df_filtered = db.read_with_filter("Orders", conn_str, "OrderAmount", "> 500")

# Insert data
db.insert_dataframe("NewTable", df, conn_str)

# Delete rows
deleted_count = db.delete_with_filter("Orders", conn_str, "OrderStatus", "= 'Cancelled'")
```

## Documentation

- [Installation](installation.md) - Get started with the module
- [Usage Guide](usage.md) - Detailed usage examples
- [API Reference](api/functions.md) - Complete API documentation
- [Building & Deployment](building.md) - Build and package information

## Requirements

- Python 3.10+
- pyodbc
- pandas
- ODBC Driver 17 for SQL Server

## License

This project is licensed under the MIT License - see the LICENSE file for details.
