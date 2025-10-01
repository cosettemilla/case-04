import json
import hashlib
from pathlib import Path
from datetime import datetime

# Resolve paths relative to this file (works no matter the CWD)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "survey.ndjson"

# Ensure directory exists (fixes 500 on first write)
DATA_DIR.mkdir(parents=True, exist_ok=True)

def hash_value(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def append_json_line(record: dict):
    # Hash sensitive fields
    if "email" in record and record["email"] is not None:
        record["email"] = hash_value(record["email"])
    if "age" in record and record["age"] is not None:
        record["age"] = hash_value(str(record["age"]))

    # Serialize datetimes
    if "received_at" in record and isinstance(record["received_at"], datetime):
        record["received_at"] = record["received_at"].isoformat()

    # Append as NDJSON
    with DATA_FILE.open("a", encoding="utf-8") as f:
        json.dump(record, f)
        f.write("\n")

