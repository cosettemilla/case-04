from datetime import datetime, timezone
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import ValidationError
from models import SurveySubmission, StoredSurveyRecord
from storage import append_json_line, hash_value

app = Flask(__name__)
# Allow cross-origin requests so the static HTML can POST from localhost or file://
CORS(app, resources={r"/v1/*": {"origins": "*"}})


@app.route("/ping", methods=["GET"])
def ping():
    """Simple health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "API is alive",
        "utc_time": datetime.now(timezone.utc).isoformat()
    })


@app.post("/v1/survey")
def submit_survey():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({
            "error": "invalid_json",
            "detail": "Body must be application/json"
        }), 400

    # Add user_agent before validation
    payload["user_agent"] = request.headers.get("User-Agent", "unknown")

    try:
        submission = SurveySubmission(**payload)
    except ValidationError as ve:
        return jsonify({
            "error": "validation_error",
            "detail": ve.errors()
        }), 422

    # Build stored record
    record = StoredSurveyRecord(
        **submission.dict(),
        received_at=datetime.now(timezone.utc),
        ip=request.headers.get("X-Forwarded-For", request.remote_addr or "")
    )

     # Generate submission_id if not provided
    if not record.submission_id:
        timestamp = datetime.utcnow().strftime("%Y%m%d%H")
        # Use the email (already hashed in storage) + timestamp to create a stable id
        unique_str = submission.email + timestamp
        record.submission_id = hash_value(unique_str)

    # Save record to file
    append_json_line(record.dict())

    return jsonify({
        "status": "success",
        "data": submission.dict()
    }), 201


if __name__ == "__main__":
    app.run(port=5000, debug=True)



