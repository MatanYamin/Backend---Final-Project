from flask import Flask
import flask
import json
import requests
import email_handler as email
import synCalendar as sync
import event_handler as event
import connect_database as connect
import db_handling as db
import calendar


connection = connect.connect_db()
cursor = connection.cursor()
app = Flask(__name__)


@app.route("/booking", methods=["POST"])
def booking():
    data_from_api = flask.request.data.decode()  # get the body of the request
    values = json.loads(data_from_api)  # convert to jason in order to get the fields
    print(values["price"])
    values["day"] = db.findDay(values["date"]) + ": " + values["date"].split("T")[0]
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


@app.route("/addon", methods=["POST"])
def addons_title():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    addons = db.fetch_all_addons(cursor, values['add'])
    return flask.jsonify(addons)


@app.route("/prices", methods=["POST"])
def prices():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    price = db.get_service_price(cursor, values["prices"])
    return flask.jsonify(price)


@app.route("/prices/addon", methods=["POST"])
def addon_price():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    price = db.get_addons_price(cursor, values["addon"])
    return flask.jsonify(price)


if __name__ == "__main__":
    app.run(debug=True)