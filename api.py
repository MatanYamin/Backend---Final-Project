from flask import Flask
import requests

app = Flask(__name__)


@app.route("/", methods=["POST"])
def home():
    response = requests.get("http://127.0.0.1:5000/")
    print("matan")
    print(response.status_code)
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)