from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Backend API is running"})

@app.route("/auth")
def call_auth():
    r = requests.get("http://auth-service:6000/")
    return r.json()

@app.route("/payments")
def call_payments():
    r = requests.get("http://payments-service:7000/")
    return r.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
