from flask import Flask
import flask
import json
import email_handler as email
# import syn_calendar as sync
import event_handler as event
import connect_database as connect
import db_handling as db
from flask_cors import CORS, cross_origin


app = Flask(__name__)
# cors = CORS(app, resources={r"/foo": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


@app.route("/booking", methods=["POST"])
@cross_origin()
def booking():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()  # get the body of the request
    values = json.loads(data_from_api)  # convert to jason in order to get the fields
    db.add_new_booking(cursor, connection, values)
    new_day = db.day_plus_one(values["date"].split("T")[0])
    values["day"] = db.findDay(values["date"]) + ": " + new_day
    email.email_handle(values)  # email handler sends emails to customer and manager
    values["date"] = db.handle_time(cursor, connection, values["date"], values["hour"])  # handle time changes the date
    # service = sync.syncalendar_and_service()
    event.create_event_and_insert(values)  # create event in the calendar
    connection.close()
    return 'OK'


# when we get into the first step, we will want all services displayed for specific category
@app.route("/services", methods=["POST"])
@cross_origin()
def get_service_by_category():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    services = db.get_service_by_category(cursor, connection, values['title'])
    connection.close()
    return flask.jsonify(services)


# getting all categories name
@app.route("/get/categories", methods=["GET"])
@cross_origin()
def get_all_categories():
    connection = connect.connect_db()
    cursor = connection.cursor()
    categories = db.get_all_categories(cursor, connection)
    connection.close()
    return flask.jsonify(categories)


# adding new service to DB
@app.route("/post/service", methods=["POST"])
@cross_origin()
def add_new_service():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    db.add_new_service(cursor, connection, values)
    connection.close()
    return "ok"


# getting all addons
@app.route("/get/addons", methods=["GET"])
@cross_origin()
def get_all_addons():
    connection = connect.connect_db()
    cursor = connection.cursor()
    addons = db.get_all_addons(cursor, connection)
    connection.close()
    return flask.jsonify(addons)


# deleting a specific addon
@app.route("/delete/addon", methods=["DELETE"])
@cross_origin()
def delete_addon():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    db.delete_addon(cursor, connection, values["addon_name"])
    connection.close()
    return "ok"


# get all services
@app.route("/get/services", methods=["GET"])
@cross_origin()
def get_services():
    connection = connect.connect_db()
    cursor = connection.cursor()
    services = db.get_all_services(cursor, connection)
    connection.close()
    return flask.jsonify(services)


# adding new addon with the relevant values
@app.route("/put/addon", methods=["PUT"])
@cross_origin()
def add_new_addon():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    db.add_new_addon(cursor, connection, values)
    connection.close()
    return "ok"


# delete specific service
@app.route("/delete/service", methods=["DELETE"])
@cross_origin()
def delete_service():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()  # getting the body request
    values = json.loads(data_from_api)
    db.delete_service(cursor, connection, values["service_name"])
    connection.close()
    return "ok"


# returning all addons that belong to a service that being sent from the frontend
@app.route("/addon", methods=["POST"])
@cross_origin()
def addons_title():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    addons = db.get_all_addons_by_service(cursor, connection, values['add'])
    connection.close()
    return flask.jsonify(addons)


# get price for service
@app.route("/prices", methods=["POST"])
@cross_origin()
def price_and_details():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    price, dits, images = db.get_service_price_and_description(cursor, connection, values["service"])
    connection.close()
    return flask.jsonify(price, dits, images)


# get price for service
@app.route("/admin/prices", methods=["POST"])
@cross_origin()
def get_service_price():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    price = db.get_service_price(cursor, connection, values["prices"])
    connection.close()
    return flask.jsonify(price)


# getting price of a certain addon
@app.route("/prices/addon", methods=["POST"])
@cross_origin()
def addon_price():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    price = db.get_addon_price(cursor, connection, values["addon"])
    connection.close()
    return flask.jsonify(price)


# this date will be exclude from calendar
@app.route("/put/disable_date", methods=["PUT"])
@cross_origin()
def disable_date():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    day = values["date"].split("T")
    new_day = db.day_plus_one(day[0])
    db.add_date_to_be_disable(cursor, connection, new_day)
    connection.close()
    return "ok"


# this date will be exclude from calendar
@app.route("/delete/activate_date", methods=["DELETE"])
@cross_origin()
def activate_date():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    day = values["date"].split("T")
    new_day = db.day_plus_one(day[0])
    db.delete_disabled_date(cursor, connection, new_day)
    connection.close()
    return "ok"


# will get all days to be disable from DB
# @app.route("/get/disable_date", methods=["GET"])
# @cross_origin()
# def get_disable_dates():
#     connection = connect.connect_db()
#     cursor = connection.cursor()
#     disabled_days = db.get_all_disabled_dates(cursor, connection)
#     connection.close()
#     return flask.jsonify(disabled_days)


# will get a day and return the available hours for that day
@app.route("/post/hours", methods=["POST"])
@cross_origin()
def get_hours_for_day():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    day = values["date"].split("T")
    new_day = db.day_plus_one(day[0])
    hours = db.get_hours_for_day(cursor, connection, new_day)
    connection.close()
    return flask.jsonify(hours)


# will block hour for giving services
@app.route("/post/new_hours", methods=["POST"])
@cross_origin()
def block_hour():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    day = values["date"].split("T")
    new_day = db.day_plus_one(day[0])
    hours = db.block_hour(cursor, connection, new_day, values["hour"])
    connection.close()
    return flask.jsonify(hours)


@app.route("/get/cities", methods=["GET"])
@cross_origin()
def get_all_cities():
    connection = connect.connect_db()
    cursor = connection.cursor()
    cities = db.get_all_cities(cursor, connection)
    connection.close()
    return flask.jsonify(cities)


@app.route("/", methods=["GET"])
@cross_origin()
def home_page():
    html = """\
        <html dir="RTL">
          <head> 
           <meta charset="utf-8">
           </head>
          <body style="
    text-align: center;
    font-size: 4vw;
    margin-top: 3vw;"> 
        Welcome to SkyCleaner's API 
        <br/>
            By Matan Yamin
          </body>
        </html>
        """
    return html


@app.route("/post/city", methods=["POST"])
@cross_origin()
def add_city():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.add_city(cursor, connection, values["city"], values["region"])
    connection.close()
    return "ok"


@app.route("/delete/city", methods=["DELETE"])
@cross_origin()
def delete_city():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.delete_city(cursor, connection, values["city"])
    connection.close()
    return "ok"


@app.route("/put/service_price", methods=["PUT"])
@cross_origin()
def edit_service_price():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.edit_service_price(cursor, connection, values["price"], values["service"])
    connection.close()
    return flask.jsonify(values["price"])


@app.route("/put/addon_price", methods=["PUT"])
@cross_origin()
def edit_addon_price():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.edit_addon_price(cursor, connection, values["price"], values["addon"])
    connection.close()
    return flask.jsonify(values["price"])


@app.route("/get/customers", methods=["GET"])
@cross_origin()
def get_future_customers():
    connection = connect.connect_db()
    cursor = connection.cursor()
    customers = db.get_future_customers(cursor, connection)
    connection.close()
    return flask.jsonify(customers)


@app.route("/get/all_customers", methods=["GET"])
@cross_origin()
def get_all_customers():
    connection = connect.connect_db()
    cursor = connection.cursor()
    customers = db.get_all_customers(cursor, connection)
    connection.close()
    return flask.jsonify(customers)


@app.route("/get/past_customers", methods=["GET"])
@cross_origin()
def get_past_customers():
    connection = connect.connect_db()
    cursor = connection.cursor()
    customers = db.get_past_customers(cursor, connection)
    connection.close()
    return flask.jsonify(customers)


# this is for shoing the address on the google map API
@app.route("/get/customers/address", methods=["GET"])
@cross_origin()
def get_customers_address():
    connection = connect.connect_db()
    cursor = connection.cursor()
    address, details = db.get_customers_address(cursor, connection)
    connection.close()
    return flask.jsonify(address, details)


# this is for shoing the address on the google map API
@app.route("/get/now-hours", methods=["GET"])
@cross_origin()
def get_time():
    connection = connect.connect_db()
    cursor = connection.cursor()
    time = db.get_time_for_display(cursor, connection)
    connection.close()
    return flask.jsonify(time)


# send feedback mail to customer after service
@app.route("/post/time", methods=["POST"])
@cross_origin()
def update_time():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.change_hours_for_day(cursor, connection, values["start"], values["end"], values["interval"])
    connection.close()
    return "ok"


@app.route("/delete/booking", methods=["DELETE"])
@cross_origin()
def delete_booking():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.delete_booking_and_unblock_hour(cursor, connection, values)
    connection.close()
    return "ok"


# send feedback mail to customer after service
@app.route("/post/feedback", methods=["POST"])
@cross_origin()
def send_feedback():
    connection = connect.connect_db()
    # cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    email.handle_feedback(values)
    # db.delete_booking_only(cursor, connection, values["id"])
    connection.close()
    return 'ok'


# send feedback mail to customer after service
@app.route("/put/service_description", methods=["PUT"])
@cross_origin()
def edit_description_for_service():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.edit_description_for_service(cursor, connection, values["description"], values["service"])
    connection.close()
    return 'ok'


# getting description from service
@app.route("/post/service_description", methods=["POST"])
@cross_origin()
def get_description_for_service():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    description = db.get_description_for_service(cursor, connection, values["service"])
    connection.close()
    return description


# posting new image in DB
@app.route("/post/images", methods=["POST"])
@cross_origin()
def add_image():
    connection = connect.connect_db()
    cursor = connection.cursor()
    try:
        data_from_api = flask.request.data.decode()
        values = json.loads(data_from_api)
        db.add_img_to_service(cursor, connection, values["service"], values["image"])
        connection.close()
        return 'OK'
    except Exception as e:
        return e


# posting new main image in DB for service
@app.route("/post/main_images", methods=["POST"])
@cross_origin()
def add_main_image_to_service():
    connection = connect.connect_db()
    cursor = connection.cursor()
    try:
        data_from_api = flask.request.data.decode()
        values = json.loads(data_from_api)
        db.add_main_img_to_service(cursor, connection, values["service"], values["image"])
        connection.close()
        return 'OK'
    except Exception as e:
        return e


# currently unavailable
@app.route("/post/notes", methods=["POST"])
@cross_origin()
def get_note_for_service():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    note = db.get_note(cursor, connection, values["service"])
    connection.close()
    return flask.jsonify(note)


# changes the service name
@app.route("/put/service_name", methods=["PUT"])
@cross_origin()
def edit_service_name():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    db.edit_service_name(cursor, connection, values["service"], values["newName"])
    connection.close()
    return 'ok'


# post method that receiving all unavailable dates there are
@app.route("/post/disabled_dates", methods=["POST"])
@cross_origin()
def get_disabled_dates_and_by_region():
    connection = connect.connect_db()
    cursor = connection.cursor()
    data_from_api = flask.request.data.decode()
    values = json.loads(data_from_api)
    disabled_days = db.get_all_disabled_dates(cursor, connection, values["city"])
    connection.close()
    return flask.jsonify(disabled_days)


if __name__ == "__main__":
    # app.run(debug=True, host="3.138.43.76", port=8080)
    # CORS(app)
    app.run(debug=True)
    # app.run(ssl_context='adhoc')
    # app.run(host='3.138.43.76', port=8080)
    # app.run(host="0.0.0.0", port=8080)
