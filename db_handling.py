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
    """increment day by 1"""
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


def get_category_services(cursor, service):
    """getting all services for specific category"""
    cursor.execute("SELECT Service_Name FROM Services WHERE ID_CAT = %s", (service,))
    service_vals = []
    for i in cursor.fetchall():
        service_vals.append(i[0])
    return service_vals


def get_all_addons_by_service(cursor, service):
    """get addon data for a specific service"""
    addons_vals = []
    cursor.execute("SELECT Addon_Name FROM Addons WHERE ID_SER = %s", (service,))
    for i in cursor.fetchall():
        addons_vals.append(i[0])
    return addons_vals


def get_all_addons(cursor):
    """fet all addons from DB"""
    addons = []
    cursor.execute("SELECT Addon_Name FROM Addons;")
    for i in cursor.fetchall():
        addons.append(i[0])
    return addons


def get_service_price(cursor, service):
    """get price for a specific service"""
    cursor.execute("SELECT Service_Price FROM Services WHERE ID_SER = %s", (service,))
    prices = []
    for i in cursor.fetchall():
        prices.append(i[0])
    return prices


def get_addon_price(cursor, addon):
    """get price for a specific addon"""
    cursor.execute("SELECT Addon_Price FROM Addons WHERE ID_ADD = %s", (addon,))
    prices = []
    for i in cursor.fetchall():
        prices.append(i[0])
    return prices


def get_all_categories(cursor):
    """get all the categories"""
    cursor.execute("SELECT Cat_Name FROM Categories;")
    categories = []
    for i in cursor.fetchall():
        categories.append(i[0])
    return categories


def get_all_services(cursor):
    """get all the services"""
    cursor.execute("SELECT Service_name FROM Services;")
    services = []
    for i in cursor.fetchall():
        services.append(i[0])
    return services


def add_new_service(cursor, mydb, data):
    """Adding new service from Admin panel, including price and category ID"""
    sql = "INSERT INTO Services (ID_CAT, ID_SER, Service_Name, Service_Price) VALUES (%s, %s, %s, %s)"
    val = (data["cat_name"], data["service_name"], data["service_name"], data["price"], )
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
    sql = "DELETE FROM Disabled_Dates WHERE Day = %s"
    val = (day,)
    cursor.execute(sql, val)
    mydb.commit()


def get_all_disabled_dates(cursor):
    cursor.execute("SELECT Day FROM Disabled_Dates;")
    disabled = []
    for i in cursor.fetchall():
        disabled.append(i[0])
    return disabled


def get_hours_for_day(cursor, day):
    """get hours for specific day"""
    hours = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
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
    cursor.execute("SELECT City FROM Cities;")
    cities = []
    for i in cursor.fetchall():
        cities.append(i[0])
    return cities


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


if __name__ == '__main__':
    cursor, connection = connect_db()  # connect to DB

