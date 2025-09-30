import json
import hashlib
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).parent / "data" / "survey.ndjson"

def hash_value(value: str) -> str:
    """Return a SHA256 hash of the given string."""
    return hashlib.sha256(value.encode()).hexdigest()

def append_json_line(record: dict):
    # Hash sensitive fields
    if "email" in record:
        record["email"] = hash_value(record["email"])
    if "age" in record and record["age"] is not None:
        record["age"] = hash_value(str(record["age"]))

    # Convert datetime fields to ISO strings
    if "received_at" in record and isinstance(record["received_at"], datetime):
        record["received_at"] = record["received_at"].isoformat()

    # Append record to survey.ndjson
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        json.dump(record, f)
        f.write("\n")
