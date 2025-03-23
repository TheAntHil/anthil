from flask import Flask, request

app = Flask(__name__)

@app.route("/api/v1/srv/runs/", methods=["POST"])
def index():
    data = request.get_json()
    print(data)  
    return data