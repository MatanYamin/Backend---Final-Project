from flask import Flask
import flask
import json
import requests
import email_handler as email


app = Flask(__name__)


@app.route("/", methods=["POST"])
def home():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    email.email_handle(values)
    email_dict = {}  # will hold all email paramaters
    # email_dict["fullName"] = valus["full"]
    # print(y["fullName"])
    # print(y["email"])
    # print(y["fullAddress"])




if __name__ == "__main__":
    app.run(debug=True)