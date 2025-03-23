from flask import Flask, request
from receives_a_signal.signal_handler import signal_processing

app = Flask(__name__)

@app.route("/api/v1/srv/runs/", methods=["POST"])
def index():
    data = request.get_json()
    result = signal_processing(data)
    print(result)  
    return data