from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def auth_home():
    return jsonify({"auth": "Auth service running", "status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
