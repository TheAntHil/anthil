import uuid

def processing_signal(data: dict) -> dict:
    status = data["status"]
    start_time = data["start_time"]
    run_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())

    result = {
        "run_id": run_id,
        "job_id": job_id,
        "status": status,
        "start_time": start_time
    }
 
    return result