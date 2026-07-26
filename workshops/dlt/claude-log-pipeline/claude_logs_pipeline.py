import json
from pathlib import Path
from typing import Iterator, Dict, Any
import dlt

@dlt.resource(
    name="claude_project_logs",
    write_disposition="append"
)
def extract_claude_logs() -> Iterator[Dict[str, Any]]:
    """Scans all standard Windows locations where Claude Code stores session history and logs."""
    home_dir = Path.home()
    appdata_dir = Path.home() / "AppData" / "Roaming" / "Claude"
    
    # Candidate log directories for Claude Code on Windows
    candidate_dirs = [
        home_dir / ".claude" / "projects",
        home_dir / ".claude" / "logs",
        home_dir / ".claude" / "history",
        home_dir / ".claude" / "sessions",
        appdata_dir / "logs",
        appdata_dir / "history",
    ]

    found_files = []
    for d in candidate_dirs:
        if d.exists():
            files = list(d.rglob("*.json*"))
            if files:
                print(f"Found {len(files)} log file(s) in: {d}")
                found_files.extend(files)

    if not found_files:
        print(f"No log files found. Scanned: {[str(d) for d in candidate_dirs if d.exists()]}")
        return

    for file_path in found_files:
        if "settings" in file_path.name or "config" in file_path.name:
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                continue

            try:
                data = json.loads(content)
                if isinstance(data, list):
                    for record in data:
                        if isinstance(record, dict):
                            record["_file_name"] = file_path.name
                            yield record
                elif isinstance(data, dict):
                    data["_file_name"] = file_path.name
                    yield data
            except json.JSONDecodeError:
                f.seek(0)
                for line_number, line in enumerate(f, start=1):
                    line = line.strip()
                    if line:
                        try:
                            record = json.loads(line)
                            if isinstance(record, dict):
                                record["_file_name"] = file_path.name
                                record["_line_number"] = line_number
                                yield record
                        except json.JSONDecodeError:
                            continue

def run_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="claude_agent_logs",
        destination="duckdb",
        dataset_name="agent_telemetry"
    )

    load_info = pipeline.run(extract_claude_logs())
    print(load_info)

if __name__ == "__main__":
    run_pipeline()