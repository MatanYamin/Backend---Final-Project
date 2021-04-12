# Programmed by Matan Yamin - Final Project.
import connect_database as connect
from datetime import datetime, timedelta


def connect_db():
    """connects to DB, here wer'e connecting to DB using 'connect_database'
    and ther returning the connection inorder to fetch data"""
    connection = connect.connect_db()
    cursor = connection.cursor()
    return cursor, connection


def day_plus_one(day):
    """increment day by 1 because that the calendar input is returning 1 day before"""
    date = datetime.strptime(day, "%Y-%m-%d")
    modified_date = date + timedelta(days=1)
    str_date = str(modified_date)
    splited = str_date.split(" ")
    return splited[0]


def handle_time(cursor, mydb, time, hour):
    """changing the time format for the event creation"""
    temp = time.split("T")
    new_day = day_plus_one(temp[0])
    sql = "INSERT INTO Available_Dates (day_id, Hour) VALUES (%s, %s)"
    val = (new_day, hour,)
    cursor.execute(sql, val)
    mydb.commit()
    new_day += "T" + hour + ":00"
    return new_day


def block_hour(cursor, mydb, date, hour):
    """this func gets a specific hour from admin and block it to the calendar"""
    sql = "INSERT INTO Available_Dates (day_id, Hour) VALUES (%s, %s)"
    val = (date, hour,)
    cursor.execute(sql, val)
    mydb.commit()


def findDay(date):
    """Get the week day from a certain date and translate it to hebrew"""
    date = date.split("T")
    day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = datetime.strptime(date[0], '%Y-%m-%d').weekday()
    day = day_name[day]
    if day == "Sunday":
        day = "יום ראשון"
    elif day == "Monday":
        day = "יום שני"
    elif day == "Tuesday":
        day = "יום שלישי"
    elif day == "Wednesday":
        day = "יום רביעי"
    elif day == "Thursday":
        day = "יום חמישי"
    elif day == "Friday":
        day = "יום שישי"
    elif day == "Saturday":
        day = "יום שבת"
    return day


def get_service_by_category(cursor, mydb, service):
    """getting all services for specific category"""
    cursor.execute("SELECT Service_Name FROM Services WHERE ID_CAT = %s", (service,))
    service_vals = []
    for i in cursor.fetchall():
        service_vals.append(i[0])
    mydb.commit()
    return service_vals


def get_all_addons_by_service(cursor, mydb, service):
    """get addon data for a specific service"""
    addons_vals = []
    cursor.execute("SELECT Addon_Name FROM Addons WHERE ID_SER = %s", (service,))
    for i in cursor.fetchall():
        addons_vals.append(i[0])
    mydb.commit()
    return addons_vals


def get_all_addons(cursor, mydb):
    """fet all addons from DB"""
    addons = []
    cursor.execute("SELECT Addon_Name FROM Addons;")
    for i in cursor.fetchall():
        addons.append(i[0])
    mydb.commit()
    return addons


def get_service_price_and_description(cursor, mydb, service):
    """get price for a specific service"""
    cursor.execute("SELECT Service_Price, Service_Description FROM Services WHERE ID_SER = %s", (service,))
    prices = []
    dits = []
    for i in cursor.fetchall():
        prices.append(i[0])
        dits.append(i[1])
    cursor.execute("SELECT image_url FROM Images WHERE ID_SER = %s", (service,))
    images = []
    for i in cursor.fetchall():
        images.append(i[0])
    mydb.commit()
    return prices, dits, images


def get_service_price(cursor, mydb, service):
    """get price for a specific service"""
    cursor.execute("SELECT Service_Price FROM Services WHERE ID_SER = %s", (service,))
    prices = []
    for i in cursor.fetchall():
        prices.append(i[0])
    mydb.commit()
    return prices


def get_addon_price(cursor, mydb, addon):
    """get price for a specific addon"""
    cursor.execute("SELECT Addon_Price FROM Addons WHERE ID_ADD = %s", (addon,))
    prices = []
    for i in cursor.fetchall():
        prices.append(i[0])
    mydb.commit()
    return prices


def get_all_categories(cursor, mydb):
    """get all the categories"""
    cursor.execute("SELECT Cat_Name FROM Categories;")
    categories = []
    for i in cursor.fetchall():
        categories.append(i[0])
    mydb.commit()
    return categories


def get_all_services(cursor, mydb):
    """get all the services"""
    cursor.execute("SELECT Service_name FROM Services;")
    services = []
    for i in cursor.fetchall():
        services.append(i[0])
    mydb.commit()
    return services


def add_new_service(cursor, mydb, data):
    """Adding new service from Admin panel, including price and category ID"""
    sql = "INSERT INTO Services (ID_CAT, ID_SER, Service_Name, Service_Description, Service_Price) VALUES (%s, %s, %s, %s, %s)"
    val = (data["cat_name"], data["service_name"], data["service_name"], data["description"], data["price"], )
    if data["image"]:
        add_img_to_service(cursor, mydb, data["service_name"], data["image"])
    cursor.execute(sql, val)
    mydb.commit()


def add_new_addon(cursor, mydb, data):
    """Adding a new addon for a certain service"""
    sql = "INSERT INTO Addons (ID_SER, ID_ADD, Addon_Name, Addon_Price) VALUES (%s, %s, %s, %s)"
    val = (data["service_name"], data["addon_name"], data["addon_name"], data["price"],)
    cursor.execute(sql, val)
    mydb.commit()


def delete_service(cursor, mydb, service):
    """deleting a service from admin panel"""
    sql = "DELETE FROM Addons WHERE ID_SER = %s"  # first delete the addons
    val = (service,)
    cursor.execute(sql, val)
    sql = "DELETE FROM Services WHERE ID_SER = %s"
    val = (service,)
    cursor.execute(sql, val)
    mydb.commit()


def delete_addon(cursor, mydb, addon):
    """deleting a specific addon"""
    sql = "DELETE FROM Addons WHERE ID_ADD = %s"
    val = (addon,)
    cursor.execute(sql, val)
    mydb.commit()


def add_date_to_be_disable(cursor, mydb, day):
    """adding date to be disabled to the DB"""
    sql = "INSERT INTO Disabled_Dates (Day) VALUES (%s)"
    val = (day, )
    cursor.execute(sql, val)
    mydb.commit()


def delete_disabled_date(cursor, mydb, day):
    """this func realeases a disabled date and delete it from the db"""
    sql = "DELETE FROM Disabled_Dates WHERE Day = %s"
    val = (day,)
    cursor.execute(sql, val)
    mydb.commit()


def get_all_disabled_dates(cursor, mydb):
    """this func returns all dates that are disabled for work by the manager
       later, the calendar will read those hours and block them for everyone"""
    cursor.execute("SELECT Day FROM Disabled_Dates;")
    disabled = []
    for i in cursor.fetchall():
        disabled.append(i[0])
    mydb.commit()
    return disabled


def get_hours_for_day(cursor, day):
    """get hours for specific day"""
    # hours = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
    hours = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00"]
    day_hours = []
    # this is the hours that are taken
    cursor.execute("SELECT Hour FROM Available_Dates WHERE day_id = %s", (day,))
    for i in cursor.fetchall():
        day_hours.append(i[0])
    for i in day_hours:
        if i in hours:
            hours.remove(i)
    return hours


def get_all_cities(cursor):
    """this func gets all cities and sort them alphabet"""
    cursor.execute("SELECT City FROM Cities;")
    cities = []
    fetched_data = cursor.fetchall()
    for city in fetched_data:
        cities.append(city[0])
    soring = sorted(cities)
    return soring


def add_city(cursor, mydb, city):
    sql = "INSERT INTO Cities (City) VALUES (%s)"
    val = (city,)
    cursor.execute(sql, val)
    mydb.commit()


def delete_city(cursor, mydb, city):
    sql = "DELETE FROM Cities WHERE City = %s"
    val = (city,)
    cursor.execute(sql, val)
    mydb.commit()


def edit_service_price(cursor, mydb, price, service):
    """this func updates service's price"""
    sql = "UPDATE Services SET Service_Price = %s WHERE Service_Name = %s"
    val = (price, service)
    cursor.execute(sql, val)
    mydb.commit()


def edit_description_for_service(cursor, mydb, desc, service):
    """will change description for service"""
    sql = "UPDATE Services SET Service_Description = %s WHERE Service_Name = %s"
    val = (desc, service)
    cursor.execute(sql, val)
    mydb.commit()


def edit_addon_price(cursor, mydb, price, addon):
    """this func gets addon name and update his price"""
    sql = "UPDATE Addons SET Addon_Price = %s WHERE Addon_Name = %s"
    val = (price, addon)
    cursor.execute(sql, val)
    mydb.commit()


def get_values(cursor, mydb, values):
    """will get all values from the booking and add it to DB"""
    hold_data = {}
    hold_data["full_name"] = values["fullName"]
    hold_data["email"] = values["email"]
    hold_data["phone"] = values["phone"]
    hold_data["address"] = values["fullAddress"]
    hold_data["service"] = values["service"] + " " + values["addons"]
    hold_data["date"] = day_plus_one(values["date"].split("T")[0])
    hold_data["hour"] = values["hour"]
    hold_data["price"] = values["price"]
    hold_data["comments"] = values["comments"]
    add_new_booking(cursor, mydb, hold_data)


def add_new_booking(cursor, mydb, data):
    """will add the booking details to "Customers" table in DB"""
    sql = "INSERT INTO Customers (Full_Name, Email, Phone, Address, Service, Date, Hour, Price, Comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (data["full_name"], data["email"], data["phone"], data["address"], data["service"], data["date"], data["hour"], data["price"], data["comments"], )
    cursor.execute(sql, val)
    mydb.commit()


def get_all_customers(cursor):
    """get all customers details from db for displaying in the table"""
    cursor.execute("SELECT * FROM Customers;")
    customers = []
    for i in cursor.fetchall():
        customers.append(list(i))
    return customers


def unblock_hour(cursor, mydb, data):
    """this function frees hour after booking is deleted"""
    cursor.execute("DELETE FROM Available_Dates WHERE day_id = %s AND Hour = %s", (data["day"], data["hour"]))
    mydb.commit()


def delete_booking_and_unblock_hour(cursor, mydb, data):
    """deleting a service from admin panel"""
    sql = "DELETE FROM Customers WHERE id = %s"
    val = (data["id"],)
    cursor.execute(sql, val)
    # mydb.commit()
    unblock_hour(cursor, mydb, data)


def delete_booking_only(cursor, mydb, id):
    """will delete booking only"""
    sql = "DELETE FROM Customers WHERE id = %s"
    val = (id,)
    cursor.execute(sql, val)
    mydb.commit()


def add_img_to_service(cursor, mydb, service, img):
    """this func adds image to certain seervice"""
    sql = "INSERT INTO Images (ID_SER, image_url) VALUES (%s, %s)"
    val = (service, img)
    cursor.execute(sql, val)
    mydb.commit()


def get_images_for_service(cursor, mydb, service):
    """this func gives all images that belong to certain service"""
    images = []
    cursor.execute("SELECT image_rl FROM Images WHERE ID_SER = %s", (service,))
    for i in cursor.fetchall():
        images.append(i[0])
    mydb.commit()
    return images


if __name__ == '__main__':
    cursor, connection = connect_db()  # connect to DB
