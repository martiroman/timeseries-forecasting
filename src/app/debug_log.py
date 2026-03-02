import json
import time


# region agent log
def debug_log(*, session_id: str, run_id: str, hypothesis_id: str, location: str, message: str, data: dict):
    """
    Append a single NDJSON log line to the workspace log file.
    IMPORTANT: Do not log secrets (tokens, passwords, keys).
    """
    payload = {
        "sessionId": session_id,
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data or {},
        "timestamp": int(time.time() * 1000),
    }
    with open("debug-716c18.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
# endregion

