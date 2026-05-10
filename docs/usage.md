# Usage Guide

## Connection String Setup

To use `sql_database_utils`, you'll need a valid ODBC connection string to your SQL Server database.

### Connection String Format

```
DRIVER={ODBC Driver 17 for SQL Server};SERVER=server_name;DATABASE=database_name;UID=username;PWD=password
```

### Example Connection Strings

**Local SQL Server:**
```python
conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MyDatabase;UID=sa;PWD=password"
```

**Azure SQL Database:**
```python
conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=myserver.database.windows.net;DATABASE=MyDatabase;UID=user@myserver;PWD=password"
```

**Using Windows Authentication:**
```python
conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes"
```

## Reading Data

### Read Entire Table

Use `read_table()` to read an entire table into a pandas DataFrame:

```python
import sql_database_utils as db

conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MyDB;UID=user;PWD=password"

# Read entire table
df = db.read_table("Customers", conn_str)
print(df.head())
```

### Read with Filter

Use `read_with_filter()` to read only rows that match a condition:

```python
# Read orders with amount > 500
df_large_orders = db.read_with_filter(
    "Orders", 
    conn_str, 
    "OrderAmount", 
    "> 500"
)

# Read specific customer
df_customer = db.read_with_filter(
    "Customers", 
    conn_str, 
    "CustomerID", 
    "= 123"
)

# Read by date range
df_recent = db.read_with_filter(
    "TransactionLog", 
    conn_str, 
    "TransactionDate", 
    ">= '2024-01-01'"
)
```

## Writing Data

### Insert DataFrame

Use `insert_dataframe()` to insert data from a pandas DataFrame into a SQL Server table:

```python
import pandas as pd

# Create a sample DataFrame
df = pd.DataFrame({
    'CustomerID': [1, 2, 3],
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Email': ['alice@example.com', 'bob@example.com', 'charlie@example.com']
})

# Insert into table
db.insert_dataframe("Customers", df, conn_str)
```

The function will:

- **Retrieve the table schema** from the database
- **Validate columns** - ensures no extra columns exist in the DataFrame
- **Auto-fill missing columns** with NULL values
- **Use parameterized queries** to prevent SQL injection
- **Insert row-by-row** for safe operations

!!! note
    For large batch inserts (>10,000 rows), consider breaking the DataFrame into smaller chunks for better performance.

## Deleting Data

Use `delete_with_filter()` to delete rows matching a condition:

```python
# Delete cancelled orders
deleted_count = db.delete_with_filter(
    "Orders",
    conn_str,
    "OrderStatus",
    "= 'Cancelled'"
)

print(f"{deleted_count} rows deleted")

# Delete old log entries
deleted_count = db.delete_with_filter(
    "TransactionLog",
    conn_str,
    "TransactionDate",
    "< '2020-01-01'"
)

print(f"Deleted {deleted_count} old transactions")
```

## Best Practices

### Security

!!! warning
    Always use parameterized queries and avoid string concatenation for user input. The module's functions are designed to use parameterized queries internally.

### Performance

- **Reading**: For large tables, use filtering to reduce memory usage
- **Inserting**: Insert dataframes in batches of 1,000-5,000 rows for optimal speed
- **Deleting**: Test your WHERE conditions carefully before executing

### Error Handling

```python
import sql_database_utils as db

try:
    df = db.read_table("NonExistentTable", conn_str)
except Exception as e:
    print(f"Error reading table: {e}")

try:
    db.insert_dataframe("Customers", df, conn_str)
except Exception as e:
    print(f"Error inserting data: {e}")
```

## Examples

### Data Pipeline Example

```python
import sql_database_utils as db
import pandas as pd

conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MyDB;UID=user;PWD=password"

# 1. Read raw data
raw_df = db.read_table("RawData", conn_str)

# 2. Process data
processed_df = raw_df[raw_df['Amount'] > 0].copy()
processed_df['Date'] = pd.to_datetime(processed_df['Date'])

# 3. Store processed data
db.insert_dataframe("ProcessedData", processed_df, conn_str)

# 4. Clean up old entries
deleted = db.delete_with_filter("RawData", conn_str, "Status", "= 'Processed'")
print(f"Cleaned up {deleted} records")
```

### Bulk Data Migration

```python
# Read from source table
df = db.read_with_filter(
    "SourceTable",
    conn_str_source,
    "Year",
    ">= 2023"
)

# Insert to destination table
db.insert_dataframe("DestinationTable", df, conn_str_destination)

print(f"Migrated {len(df)} records")
```
