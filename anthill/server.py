from flask import Flask, request, jsonify
import logging
from anthill.signal_handler import process_signal
#from anthill.streaming_updates_signal_handler import updates_stream


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)
app = Flask(__name__)
#received_data = []


@app.route("/api/v1/srv/runs/", methods=["POST"])
def index():
    data = request.get_json()
    logger.info(f"Received data: {data}")
    try:
        result = process_signal(data)
        logger.info(f"Processing result: {result}")
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500


# @app.route("/api/v1/srv/runs/", methods=["GET"])
# def stream():
#     data = request.args
#     return jsonify(data), 200
