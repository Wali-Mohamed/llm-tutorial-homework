import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import duckdb
    import marimo as mo

    # Initialize app
    app = mo.App(width="medium")


    # Connect to your extracted DuckDB database
    db_path = r".dlt\data\dev\agent_logs.duckdb"
    conn = duckdb.connect(db_path)

    # Fetch schema dynamically
    schema_query = "SELECT table_schema FROM information_schema.tables WHERE table_name = 'messages' LIMIT 1"
    schema_name = conn.execute(schema_query).fetchone()[0]
    return conn, mo, schema_name


@app.cell
def _():
    import duckdb
    import marimo as mo

    # Initialize app
    app = mo.App(width="medium")
    return (mo,)


@app.cell
def _(conn, mo, schema_name):
    # Query summary metrics
    total_msgs = conn.execute(
        f"SELECT COUNT(*) FROM {schema_name}.messages"
    ).fetchone()[0]

    type_counts_df = conn.execute(f"""
        SELECT 
            type AS content_type,
            COUNT(*) AS total_count
        FROM {schema_name}.messages__message__content
        GROUP BY type
        ORDER BY total_count DESC
    """).df()

    tool_uses_df = conn.execute(f"""
        SELECT 
            _dlt_parent_id,
            type
        FROM {schema_name}.messages__message__content
        WHERE type = 'tool_use'
    """).df()

    # Build Stat Widgets
    stat_row = mo.hstack(
        [
            mo.stat(value=str(total_msgs), label="Total Sessions"),
            mo.stat(
                value=str(len(type_counts_df)), label="Unique Content Types"
            ),
            mo.stat(value=str(len(tool_uses_df)), label="Tool Executions"),
        ],
        justify="start",
    )

    # Render Dashboard Components
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(f"""SELECT * FROM """)
    return


if __name__ == "__main__":
    app.run()
