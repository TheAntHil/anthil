from flask import Flask, request, jsonify
import logging
from anthill.signal_handler import process_signal
from anthill.run_handler import filter_runs, sorter_runs
from datetime import datetime as dt


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)
app = Flask(__name__)
runs = []


@app.route("/api/v1/srv/runs/", methods=["POST"])
def index():
    data = request.get_json()
    logger.info(f"Received data: {data}")
    try:
        result = process_signal(data)
        logger.info(f"Processing result: {result}")
        runs.append(result)
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/srv/runs/", methods=["GET"])
def get_runs():
    after = dt.fromisoformat(request.args.get("after").replace(" ", "+"))
    sort = request.args.get("orderby")
    logger.info(f"Received request, parameters: after={after}, sort={sort}")
    try:
        filtered_run = filter_runs(runs, after)
        sorted_result = sorter_runs(filtered_run, sort)
        logger.info(f"Filtered and sorted runs: {sorted_result}")
        return jsonify(sorted_result), 200
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
