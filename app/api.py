from flask import Flask, request
from db import insert_scan_results

app = Flask(__name__)

# Health check / root route
@app.route('/')
def index():
    return "Port Scan API is running..."

# Endpoint to receive scan data via POST
@app.route('/submit-scan', methods=['POST'])
def submit_scan():
    payload = request.get_json(silent=True)
    if payload:
        insert_scan_results(payload)
        return {"message": "Scan stored successfully"}, 201
    return {"message": "No JSON payload received"}, 400 # 400 = bad request


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) # debug=True for development only




