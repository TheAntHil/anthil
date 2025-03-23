import uuid
from datetime import datetime

def processing_signal(data: dict) -> dict:
    status = data["status"]
    start_time = data["start_time"]
    run_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    updated_at = datetime.utcnow().isoformat() if "updated_at" in data else created_at

    result = {
        "run_id": run_id,
        "job_id": job_id,
        "status": status,
        "start_time": start_time,
        "created_at": created_at,
        "updated_at": updated_at
    }
 
    return result