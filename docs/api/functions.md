# API Reference

## Functions

### read_table

Reads an entire table from SQL Server into a pandas DataFrame.

```python
def read_table(table_name: str, conn_str: str) -> pd.DataFrame
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `table_name` | str | Name of the table to read |
| `conn_str` | str | ODBC connection string |

#### Returns

- **pd.DataFrame** - DataFrame containing the table data

#### Raises

- **Exception** - If table doesn't exist or connection fails

#### Example

```python
import sql_database_utils as db

conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MyDB;UID=user;PWD=password"
df = db.read_table("Customers", conn_str)
print(df.shape)
print(df.head())
```

---

### read_with_filter

Reads a filtered set of rows from a table using a WHERE clause.

```python
def read_with_filter(table_name: str, conn_str: str, column_name: str, condition: str) -> pd.DataFrame
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `table_name` | str | Name of the table to read |
| `conn_str` | str | ODBC connection string |
| `column_name` | str | Column name for the filter |
| `condition` | str | SQL condition (e.g., "= 'value'", "> 10") |

#### Returns

- **pd.DataFrame** - DataFrame containing filtered rows

#### Raises

- **Exception** - If column doesn't exist or query fails

#### Examples

```python
import sql_database_utils as db

conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MyDB;UID=user;PWD=password"

# Numeric comparison
df = db.read_with_filter("Orders", conn_str, "OrderAmount", "> 500")

# String matching
df = db.read_with_filter("Employees", conn_str, "Country", "= 'USA'")

# Date comparison
df = db.read_with_filter("Transactions", conn_str, "TransactionDate", ">= '2024-01-01'")
```

---

### delete_with_filter

Deletes rows from a SQL Server table based on a WHERE condition.

```python
def delete_with_filter(table_name: str, conn_str: str, column_name: str, condition: str) -> int
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `table_name` | str | Name of the table to delete from |
| `conn_str` | str | ODBC connection string |
| `column_name` | str | Column name for the filter |
| `condition` | str | SQL condition (e.g., "= 'value'", "> 10") |

#### Returns

- **int** - Number of rows deleted

#### Raises

- **Exception** - If table doesn't exist or query fails

#### Examples

```python
import sql_database_utils as db

conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MyDB;UID=user;PWD=password"

# Delete cancelled orders
deleted = db.delete_with_filter("Orders", conn_str, "Status", "= 'Cancelled'")
print(f"Deleted {deleted} orders")

# Delete old records
deleted = db.delete_with_filter("AuditLog", conn_str, "CreatedDate", "< '2020-01-01'")
print(f"Deleted {deleted} old audit records")
```

---

### insert_dataframe

Inserts data from a pandas DataFrame into a SQL Server table.

```python
def insert_dataframe(table_name: str, dataframe: pd.DataFrame, conn_str: str) -> None
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `table_name` | str | Name of the table to insert into |
| `dataframe` | pd.DataFrame | DataFrame containing data to insert |
| `conn_str` | str | ODBC connection string |

#### Process

1. **Schema Retrieval** - Fetches the table schema from the database
2. **Validation** - Checks for extra columns in the DataFrame
3. **Missing Columns** - Auto-fills missing columns with NULL
4. **Parameterized Insert** - Generates safe INSERT queries
5. **Row-by-Row Insert** - Inserts one row at a time

#### Returns

- **None**

#### Raises

- **Exception** - If table doesn't exist, has extra columns, or insert fails

#### Examples

```python
import pandas as pd
import sql_database_utils as db

conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MyDB;UID=user;PWD=password"

# Create DataFrame
df = pd.DataFrame({
    'CustomerID': [1, 2, 3],
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Email': ['alice@example.com', 'bob@example.com', 'charlie@example.com']
})

# Insert data
db.insert_dataframe("Customers", df, conn_str)
print("Data inserted successfully")
```

#### Notes

- The DataFrame columns must match the table's columns
- Missing columns in the DataFrame will be set to NULL
- Extra columns will cause an error
- Parameterized queries prevent SQL injection
- Row-by-row insertion is safe but slower; consider batching for large datasets

---

## Connection String Reference

### Format

```
DRIVER={ODBC Driver 17 for SQL Server};SERVER=server;DATABASE=database;UID=user;PWD=password
```

### Common Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `DRIVER` | ODBC driver version | `{ODBC Driver 17 for SQL Server}` |
| `SERVER` | Server address | `localhost`, `server.database.windows.net` |
| `DATABASE` | Database name | `MyDatabase` |
| `UID` | Username | `user@domain` |
| `PWD` | Password | `SecurePassword123` |
| `Trusted_Connection` | Use Windows auth | `yes` |

