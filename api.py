from flask import Flask
import flask
import json
import requests

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if flask.request.method == "POST":
        lis = flask.request.data.decode()
        y = json.loads(lis)
        print(y["fullName"])
        print(y["email"])
        print(y["fullAddress"])
    if flask.request.method == "GET":
        print("this is get")
    return "Hello, World! My name is Matan Yamin"


if __name__ == "__main__":
    app.run(debug=True)