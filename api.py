from flask import Flask
import flask
import json
import email_handler as email
import synCalendar as sync
import event_handler as event
import connect_database as connect
import db_handling as db
from flask_cors import CORS, cross_origin


connection = connect.connect_db()
cursor = connection.cursor()
app = Flask(__name__)
# cors = CORS(app, resources={r"/foo": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


@app.route("/booking", methods=["POST"])
@cross_origin()
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
@cross_origin()
def get_service_by_category():
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    services = db.get_service_by_category(cursor, values['title'])
    return flask.jsonify(services)


# getting all categories name
@app.route("/get/categories", methods=["GET"])
@cross_origin()
def get_all_categories():
    categories = db.get_all_categories(cursor)
    return flask.jsonify(categories)


# adding new service to DB
@app.route("/post/service", methods=["POST"])
@cross_origin()
def add_new_service():
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    db.add_new_service(cursor, connection, values)
    return "ok"


# getting all addons
@app.route("/get/addons", methods=["GET"])
@cross_origin()
def get_all_addons():
    addons = db.get_all_addons(cursor)
    return flask.jsonify(addons)


# deleting a specific addon
@app.route("/delete/addon", methods=["DELETE"])
@cross_origin()
def delete_addon():
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    db.delete_addon(cursor, connection, values["addon_name"])
    return "ok"


# get all services
@app.route("/get/services", methods=["GET"])
@cross_origin()
def get_services():
    services = db.get_all_services(cursor)
    return flask.jsonify(services)


@app.route("/put/addon", methods=["PUT"])
@cross_origin()
def add_new_addon():
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    db.add_new_addon(cursor, connection, values)
    return "ok"


# delete specific service
@app.route("/delete/service", methods=["DELETE"])
@cross_origin()
def delete_service():
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    db.delete_service(cursor, connection, values["service_name"])
    return "ok"


@app.route("/addon", methods=["POST"])
@cross_origin()
def addons_title():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    addons = db.get_all_addons_by_service(cursor, values['add'])
    return flask.jsonify(addons)


# get price for service
@app.route("/prices", methods=["POST"])
@cross_origin()
def price_and_details():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    price, dits, images = db.get_service_price_and_description(cursor, values["service"])
    return flask.jsonify(price, dits, images)


# get price for service
@app.route("/admin/prices", methods=["POST"])
@cross_origin()
def get_service_price():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    price = db.get_service_price(cursor, values["prices"])
    return flask.jsonify(price)


@app.route("/prices/addon", methods=["POST"])
@cross_origin()
def addon_price():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    price = db.get_addon_price(cursor, values["addon"])
    return flask.jsonify(price)


# this date will be exclude from calendar
@app.route("/put/disabledate", methods=["PUT"])
@cross_origin()
def disable_date():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    day = values["date"].split("T")
    new_day = db.day_plus_one(day[0])
    db.add_date_to_be_disable(cursor, connection, new_day)
    return "ok"


# this date will be exclude from calendar
@app.route("/delete/activatedate", methods=["DELETE"])
@cross_origin()
def activate_date():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    day = values["date"].split("T")
    new_day = db.day_plus_one(day[0])
    db.delete_disabled_date(cursor, connection, new_day)
    return "ok"


# will get all days to be disable from DB
@app.route("/get/disabledate", methods=["GET"])
@cross_origin()
def get_disable_dates():
    disabled_days = db.get_all_disabled_dates(cursor)
    return flask.jsonify(disabled_days)


# will get a day and return the available hours for that day
@app.route("/post/hours", methods=["POST"])
@cross_origin()
def get_hours_for_day():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    day = values["date"].split("T")
    new_day = db.day_plus_one(day[0])
    hours = db.get_hours_for_day(cursor, new_day)
    return flask.jsonify(hours)


# will block hour for giving services
@app.route("/post/newhours", methods=["POST"])
@cross_origin()
def block_hour():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    day = values["date"].split("T")
    new_day = db.day_plus_one(day[0])
    hours = db.block_hour(cursor, connection, new_day, values["hour"])
    return flask.jsonify(hours)


@app.route("/get/cities", methods=["GET"])
@cross_origin()
def get_all_cities():
    cities = db.get_all_cities(cursor)
    return flask.jsonify(cities)


@app.route("/get/this", methods=["GET"])
@cross_origin()
def get_something():
    return "9000"


@app.route("/post/city", methods=["POST"])
@cross_origin()
def add_city():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.add_city(cursor, connection, values["city"])
    return "ok"


@app.route("/delete/city", methods=["DELETE"])
@cross_origin()
def delete_city():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.delete_city(cursor, connection, values["city"])
    return "ok"


@app.route("/put/service_price", methods=["PUT"])
@cross_origin()
def edit_service_price():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.edit_service_price(cursor, connection, values["price"], values["service"])
    return flask.jsonify(values["price"])


@app.route("/put/addon_price", methods=["PUT"])
@cross_origin()
def edit_addon_price():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.edit_addon_price(cursor, connection, values["price"], values["addon"])
    return flask.jsonify(values["price"])


@app.route("/get/customers", methods=["GET"])
@cross_origin()
def get_all_customers():
    customers = db.get_all_customers(cursor)
    return flask.jsonify(customers)


@app.route("/delete/booking", methods=["DELETE"])
@cross_origin()
def delete_booking():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.delete_booking_and_unblock_hour(cursor, connection, values)
    return "ok"


# send feedback mail to customer after service
@app.route("/post/feedback", methods=["POST"])
@cross_origin()
def send_feedback():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    email.handle_feedback(values)
    # db.delete_booking_only(cursor, connection, values["id"])
    return 'ok'


# send feedback mail to customer after service
@app.route("/put/service_description", methods=["PUT"])
@cross_origin()
def edit_description_for_service():
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.edit_description_for_service(cursor, connection, values["description"], values["service"])
    return 'ok'


# posting new image in DB
@app.route("/post/images", methods=["POST"])
@cross_origin()
def add_image():
    print("im here")
    try:
        data_from_api = flask.request.data.decode()
        values = json.loads(data_from_api)
        db.add_img_to_service(cursor, connection, values["service"], values["image"])
        return flask.jsonify("הכל בסדק")

    except:
        return 'משהו השתבש, רענן ונסה שוב'


# @app.route("/get/images", methods=["GET"])
# def get_all_customers():
#     images = db.get(cursor)
#     return flask.jsonify(customers)


if __name__ == "__main__":
    # app.run(debug=True, host="3.138.43.76", port=8080)
    # CORS(app)
    app.run(debug=True)
    # app.run(ssl_context='adhoc')
    # app.run(host='3.138.43.76', port=8080)
    # app.run(host="0.0.0.0", port=8080)
