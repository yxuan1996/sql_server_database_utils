# Installation

## Prerequisites

Before installing `sql_database_utils`, ensure you have the following installed:

- **Python 3.10 or higher**
- **ODBC Driver 17 for SQL Server** - Required for database connectivity

### Installing ODBC Driver 17

#### On Windows
Download and install from the [Microsoft ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).

#### On macOS
```bash
# Using Homebrew
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install msodbcsql17 mssql-tools
```

#### On Linux (Ubuntu/Debian)
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
apt-get install -y msodbcsql17
```

## Installing sql_database_utils

### From PyPI (Coming Soon)
```bash
pip install sql-database-utils
```

### From GitHub Releases
```bash
pip install https://github.com/yxuan1996/sql_server_database_utils/releases/download/Production/sql_database_utils-0.2.0-py3-none-any.whl
```

### From Source

1. Clone the repository:
```bash
git clone https://github.com/yxuan1996/sql_server_database_utils.git
cd sql_server_database_utils
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the module:
```bash
pip install -e .
```

## Verifying Installation

To verify the installation was successful, try importing the module:

```python
import sql_database_utils

print(dir(sql_database_utils))
```

You should see the available functions listed.
