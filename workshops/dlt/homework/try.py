import os
import duckdb
import pandas as pd
from dotenv import load_dotenv
from logfire.experimental.query_client import LogfireQueryClient

# 1. Load variables from .env
load_dotenv()

read_token = os.getenv("LOGFIRE_READ_TOKEN")
if not read_token:
    raise ValueError("LOGFIRE_READ_TOKEN not found in .env file!")

# 2. Initialize Client
client = LogfireQueryClient(
    read_token=read_token,
    base_url="https://logfire-eu.pydantic.dev",
)

# 3. Query records
query = """
SELECT 
    start_timestamp,
    span_name,
    attributes
FROM records
ORDER BY start_timestamp DESC
LIMIT 500
"""

# Fetch JSON rows and convert to Pandas DataFrame
response = client.query_json_rows(query)
df = pd.DataFrame(response["rows"])

# 4. Save DataFrame into DuckDB
con = duckdb.connect("homework_logfire.duckdb")

# DuckDB can read 'df' directly from python memory
con.execute("CREATE TABLE IF NOT EXISTS spans AS SELECT * FROM df")

count = con.execute("SELECT COUNT(*) FROM spans").fetchone()[0]
print(f"Successfully saved {count} records into DuckDB!")

con.close()