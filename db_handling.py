# Programmed by Matan Yamin - Final Project.
import connect_database as connect
from datetime import datetime, timedelta
# import datetime
import calendar
# Here will bee all the functions that are fetching data from the DB and will handle changes


def connect_db():
    """connects to DB, here wer'e connecting to DB using 'connect_database'
    and ther returning the connection inorder to fetch data"""
    connection = connect.connect_db()
    cursor = connection.cursor()
    return cursor, connection


def handle_time(time, hour):
    """change the time format for the event creation"""
    temp = time.split("T")
    # temp[0] += "T" + hour + ":00"
    # s = '2004/03/30'
    date = datetime.strptime(temp[0], "%Y-%m-%d")
    modified_date = date + timedelta(days=1)
    str_date = str(modified_date)
    splited = str_date.split(" ")
    splited[0] += "T" + hour + ":00"
    # print(splited[0])
    return splited[0]


def findDay(date):
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


def fetch_all_services(cursor, service):
    cursor.execute("SELECT Service_Name FROM Services WHERE ID_CAT = %s", (service,))
    service_vals = []
    for i in cursor.fetchall():
        service_vals.append(i[0])
    return service_vals


def fetch_all_addons(cursor, addon):
    """get addon data for a specific service"""
    addons_vals = []
    cursor.execute("SELECT Addon_Name FROM Addons WHERE ID_SER = %s", (addon,))
    for i in cursor.fetchall():
        addons_vals.append(i[0])
    # print(addons_vals)
    return addons_vals


def get_service_price(cursor, service):
    cursor.execute("SELECT Service_Price FROM Services WHERE ID_SER = %s", (service,))
    prices = []
    for i in cursor.fetchall():
        prices.append(i[0])
    return prices


def get_addons_price(cursor, addon):
    cursor.execute("SELECT Addon_Price FROM Addons WHERE ID_ADD = %s", (addon,))
    prices = []
    for i in cursor.fetchall():
        prices.append(i[0])
    return prices


if __name__ == '__main__':
    cursor, connection = connect_db()  # connect to DB
    # fetch_all_services(cursor)

