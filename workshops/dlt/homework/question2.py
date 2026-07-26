import duckdb

# Point directly to the dlt output file
con = duckdb.connect(".dlt/data/dev/logfire_to_duckdb.duckdb")

# Count the total number of tables in the 'agent_traces' schema
result = con.execute("""
    SELECT COUNT(*) 
    FROM information_schema.tables 
    WHERE table_schema = 'agent_traces';
""").fetchone()

print(f"Total tables created by dlt: {result[0]}")
