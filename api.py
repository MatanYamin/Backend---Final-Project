from flask import Flask
import flask
import json
import requests
import email_handler as email
import synCalendar as sync
import event_handler as event
import connect_database as connect
import db_handling as db


connection = connect.connect_db()
cursor = connection.cursor()
app = Flask(__name__)


@app.route("/booking", methods=["POST"])
def booking():
    # cursor, connection = connect_db()
    # db.fetch_all_services(cursor, service_name)
    # data_list = []
    # query = "SELECT * FROM Customers;"
    # db.insert_data_list(query, data_list)
    data_from_api = flask.request.data.decode()  # get the body of the request
    values = json.loads(data_from_api)  # convert to jason in order to get the fields
    email.email_handle(values)  # email handler sends emails to customet and manager
    values["date"] = db.handle_time(values["date"], values["hour"])  # handle time changes the date
    service = sync.syncalendar_and_service()
    event.create_event_and_insert(service, values)  # create event in the calendar
    return 'OK'


@app.route("/services", methods=["POST"])  # when we get into the first step, we will want all services displayed
def service_title():
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    services = db.fetch_all_services(cursor, values['title'])
    return flask.jsonify(services)
    # post_services(services)  # this will send the data to the api
    # return 'OK'



if __name__ == "__main__":
    app.run(debug=True)