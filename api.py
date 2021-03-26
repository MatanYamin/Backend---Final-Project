from flask import Flask
import flask
import json
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
    data_from_api = flask.request.data.decode()  # get the body of the request
    values = json.loads(data_from_api)  # convert to jason in order to get the fields
    values["day"] = db.findDay(values["date"]) + ": " + values["date"].split("T")[0]
    email.email_handle(values)  # email handler sends emails to customet and manager
    values["date"] = db.handle_time(values["date"], values["hour"])  # handle time changes the date
    service = sync.syncalendar_and_service()
    event.create_event_and_insert(service, values)  # create event in the calendar
    return 'OK'


# when we get into the first step, we will want all services displayed for specific category
@app.route("/services", methods=["POST"])
def get_service_by_category():
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    services = db.get_category_services(cursor, values['title'])
    return flask.jsonify(services)


# getting all categories name
@app.route("/get/categories", methods=["GET"])
def get_all_categories():
    categories = db.get_all_categories(cursor)
    return flask.jsonify(categories)


# adding new service to DB
@app.route("/post/service", methods=["POST"])
def add_new_service():
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    db.add_new_service(cursor, connection, values)
    return "ok"


# getting all addons
@app.route("/get/addons", methods=["GET"])
def get_all_addons():
    addons = db.get_all_addons(cursor)
    return flask.jsonify(addons)


# deleting a specific addon
@app.route("/delete/addon", methods=["DELETE"])
def delete_addon():
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    db.delete_addon(cursor, connection, values["addon_name"])
    return "ok"


# get all services
@app.route("/get/services", methods=["GET"])
def get_services():
    services = db.get_all_services(cursor)
    return flask.jsonify(services)


@app.route("/put/addon", methods=["PUT"])
def add_new_addon():
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    db.add_new_addon(cursor, connection, values)
    return "ok"


# delete specific service
@app.route("/delete/service", methods=["DELETE"])
def delete_service():
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    db.delete_service(cursor, connection, values["service_name"])
    return "ok"


@app.route("/addon", methods=["POST"])
def addons_title():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    addons = db.get_all_addons_by_service(cursor, values['add'])
    return flask.jsonify(addons)


# get price for service
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
    price = db.get_addon_price(cursor, values["addon"])
    return flask.jsonify(price)


if __name__ == "__main__":
    app.run(debug=True)