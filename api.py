from flask import Flask
import flask
import json
import email_handler as email
import synCalendar as sync
import event_handler as event
import connect_database as connect
import db_handling as db
import requests
import io
import urllib.request as urllib
from PIL import Image
from urllib.request import urlopen


connection = connect.connect_db()
cursor = connection.cursor()
app = Flask(__name__)


@app.route("/booking", methods=["POST"])
def booking():
    data_from_api = flask.request.data.decode()  # get the body of the request
    values = json.loads(data_from_api)  # convert to jason in order to get the fields
    db.get_values(cursor, connection, values)
    new_day = db.day_plus_one(values["date"].split("T")[0])
    values["day"] = db.findDay(values["date"]) + ": " + new_day
    email.email_handle(values)  # email handler sends emails to customet and manager
    values["date"] = db.handle_time(cursor, connection, values["date"], values["hour"])  # handle time changes the date
    service = sync.syncalendar_and_service()
    event.create_event_and_insert(service, values)  # create event in the calendar
    return 'OK'


# when we get into the first step, we will want all services displayed for specific category
@app.route("/services", methods=["POST"])
def get_service_by_category():
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    services = db.get_service_by_category(cursor, values['title'])
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
def price_and_details():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    price, dits = db.get_service_price_and_description(cursor, values["prices"])
    return flask.jsonify(price, dits)


# get price for service
@app.route("/admin/prices", methods=["POST"])
def get_service_price():
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


# this date will be exclude from calendar
@app.route("/put/disabledate", methods=["PUT"])
def disable_date():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    day = values["date"].split("T")
    new_day = db.day_plus_one(day[0])
    db.add_date_to_be_disable(cursor, connection, new_day)
    return "ok"


# this date will be exclude from calendar
@app.route("/delete/activatedate", methods=["DELETE"])
def activate_date():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    day = values["date"].split("T")
    new_day = db.day_plus_one(day[0])
    db.delete_disabled_date(cursor, connection, new_day)
    return "ok"


# will get all days to be disable from DB
@app.route("/get/disabledate", methods=["GET"])
def get_disable_dates():
    disabled_days = db.get_all_disabled_dates(cursor)
    return flask.jsonify(disabled_days)


# will get a day and return the available hours for that day
@app.route("/post/hours", methods=["POST"])
def get_hours_for_day():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    day = values["date"].split("T")
    new_day = db.day_plus_one(day[0])
    hours = db.get_hours_for_day(cursor, new_day)
    return flask.jsonify(hours)


# will block hour for giving services
@app.route("/post/newhours", methods=["POST"])
def block_hour():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    day = values["date"].split("T")
    new_day = db.day_plus_one(day[0])
    hours = db.block_hour(cursor, connection, new_day, values["hour"])
    return flask.jsonify(hours)


@app.route("/get/cities", methods=["GET"])
def get_all_cities():
    cities = db.get_all_cities(cursor)
    return flask.jsonify(cities)


@app.route("/get/gal", methods=["GET"])
def gettt():
    return 90000


@app.route("/post/city", methods=["POST"])
def add_city():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.add_city(cursor, connection, values["city"])
    return "ok"


@app.route("/delete/city", methods=["DELETE"])
def delete_city():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.delete_city(cursor, connection, values["city"])
    return "ok"


@app.route("/put/service_price", methods=["PUT"])
def edit_service_price():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.edit_service_price(cursor, connection, values["price"], values["service"])
    return flask.jsonify(values["price"])


@app.route("/put/addon_price", methods=["PUT"])
def edit_addon_price():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.edit_addon_price(cursor, connection, values["price"], values["addon"])
    return flask.jsonify(values["price"])


@app.route("/get/customers", methods=["GET"])
def get_all_customers():
    customers = db.get_all_customers(cursor)
    return flask.jsonify(customers)


@app.route("/delete/booking", methods=["DELETE"])
def delete_booking():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.delete_booking_and_unblock_hour(cursor, connection, values)
    return "ok"


# send feedback mail to customer after service
@app.route("/post/feedback", methods=["POST"])
def send_feedback():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    email.handle_feedback(values)
    # db.delete_booking_only(cursor, connection, values["id"])
    return 'ok'


# send feedback mail to customer after service
@app.route("/put/service_description", methods=["PUT"])
def edit_description_for_service():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.edit_description_for_service(cursor, connection, values["description"], values["service"])
    return 'ok'


# # posting new image in DB
# @app.route("/post/images", methods=["POST"])
# def add_image():


if __name__ == "__main__":
    app.run(debug=True, host="3.138.43.76", port=8080)
    # app.run(debug=True)
    # app.run(host="0.0.0.0")