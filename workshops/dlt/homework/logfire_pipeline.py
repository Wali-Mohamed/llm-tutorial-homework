import os
import dlt
import duckdb
from dotenv import load_dotenv
from logfire.experimental.query_client import LogfireQueryClient

load_dotenv()

read_token = os.getenv("LOGFIRE_READ_TOKEN")
client = LogfireQueryClient(
    read_token=read_token,
    base_url="https://logfire-eu.pydantic.dev",
)

query = """
SELECT 
    start_timestamp,
    end_timestamp,
    span_name,
    attributes
FROM records
ORDER BY start_timestamp DESC
LIMIT 500
"""

response = client.query_json_rows(query)
records = response["rows"]

pipeline = dlt.pipeline(
    pipeline_name="logfire_to_duckdb",
    destination="duckdb",
    dataset_name="agent_traces",
)

# max_table_nesting prevents Windows MAX_PATH errors from super deep JSON
load_info = pipeline.run(
    dlt.resource(records, name="records", max_table_nesting=2)
)

print(load_info)