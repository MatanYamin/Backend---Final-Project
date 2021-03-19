from flask import Flask
import flask
import json
import requests
import email_handler as email
import synCalendar as sync
import event_handler as event


app = Flask(__name__)


@app.route("/", methods=["POST"])
def home():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    email.email_handle(values)
    print("start event")
    service = sync.syncalendar_and_service()
    event.create_event_and_insert(service, values)
    print("end event")
    return 'OK'
    # email_dict = {}  # will hold all email paramaters
    # email_dict["fullName"] = valus["full"]
    # print(y["fullName"])
    # print(y["email"])
    # print(y["fullAddress"])




if __name__ == "__main__":
    app.run(debug=True)