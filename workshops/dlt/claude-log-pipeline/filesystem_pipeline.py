"""
DLT pipeline to load Claude logs from local .jsonl files into DuckDB.
"""

import dlt
from dlt.sources.filesystem import filesystem, read_jsonl


def create_claude_logs_source():
    # Folder path containing your project's JSONL transcripts
    logs_dir = r"C:\Users\user\.claude\projects\C--Users-user-Documents-llm-tutorial-llm-tutorial-homework-workshops-dlt-claude-log-pipeline"

    source = (
        filesystem(bucket_url=logs_dir, file_glob="*.jsonl")
        | read_jsonl()
    ).with_name("messages")

    # Limit table nesting to depth 2 to prevent deep child tables (breaks the Windows path crash)
    source.max_table_nesting = 2
    return source


def run_pipeline():
    source = create_claude_logs_source()

    pipeline = dlt.pipeline(
        pipeline_name="agent_logs",
        destination="duckdb",
        dataset_name="agent_logs",
        dev_mode=True,
    )

    load_info = pipeline.run(source, write_disposition="replace")
    print(load_info)
    return load_info


if __name__ == "__main__":
    run_pipeline()