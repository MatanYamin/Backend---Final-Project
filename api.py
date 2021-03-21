from flask import Flask
import flask
import json
import requests
import email_handler as email
import synCalendar as sync
import event_handler as event
import connect_database as connect
import db_handling as db


def connect_db():
    """connects to DB, here wer'e connecting to DB using 'connect_database'
    and ther returning the connection inorder to fetch data"""
    connection = connect.connect_db()
    cursor = connection.cursor()
    return cursor, connection


app = Flask(__name__)


@app.route("/booking", methods=["POST"])
def home():
    # cursor, connection = connect_db()
    data_list = []
    query = "SELECT * FROM Customers;"
    db.insert_data_list(query, data_list)
    print(data_list)
    ############### OK
    data_from_api = flask.request.data.decode()  # get the body of the request
    values = json.loads(data_from_api)  # convert to jason in order to get the fields
    email.email_handle(values)  # email handler sends emails to customet and manager
    values["date"] = handle_time(values["date"], values["hour"])  # handle time changes the date
    service = sync.syncalendar_and_service()
    event.create_event_and_insert(service, values)  # create event in the calendar
    # print("end event")
    ################ OK
    return 'OK'


def handle_time(time, hour):
    """change the time format for the event creation"""
    temp = time.split("T")
    temp[0] += "T" + hour + ":00"
    return temp[0]


if __name__ == "__main__":
    #
    app.run(debug=True)