# Programmed by Matan Yamin - Final Project.
import connect_database as connect
from datetime import datetime, timedelta, date
import time


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
    new_date = day_plus_one(date[0])
    day = datetime.strptime(new_date, '%Y-%m-%d').weekday()
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


def get_service_by_category(cursor, mydb, category):
    """getting all services for specific category"""
    cursor.execute("SELECT Service_Name, Service_Image FROM Services WHERE ID_CAT = %s", (category,))
    service_vals = []
    default_image = "https://s3-us-west-2.amazonaws.com/melingoimages/Images/87718.jpg"
    for i in cursor.fetchall():
        if(i[1]):
            service_vals.append((i[0], i[1]))
        else:
            service_vals.append((i[0], default_image))
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
    cursor.execute("SELECT Addon_Price FROM Addons WHERE Addon_Name = %s", (addon,))
    prices = []
    for i in cursor.fetchall():
        prices.append(i[0])
        break
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
    default_image = "https://s3-us-west-2.amazonaws.com/melingoimages/Images/87718.jpg"
    if data["image"]:
        sql = "INSERT INTO Services (ID_CAT, ID_SER, Service_Name, Service_Description, Service_Price, Service_Image) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (data["cat_name"], data["service_name"], data["service_name"], data["description"], data["price"], data["image"])
    else:
        sql = "INSERT INTO Services (ID_CAT, ID_SER, Service_Name, Service_Description, Service_Price, Service_Image) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (data["cat_name"], data["service_name"], data["service_name"], data["description"], data["price"], default_image)
    cursor.execute(sql, val)
    mydb.commit()


def add_new_addon(cursor, mydb, data):
    """Adding a new addon for a certain service"""
    sql = "INSERT INTO Addons (ID_SER, Addon_Name, Addon_Price) VALUES (%s, %s, %s)"
    val = (data["service_name"], data["addon_name"], data["price"],)
    cursor.execute(sql, val)
    mydb.commit()


def delete_service(cursor, mydb, service):
    """deleting a service from admin's panel"""
    sql = "SELECT ID_SER FROM Services WHERE Service_Name = %s"
    val = (service,)
    cursor.execute(sql, val)
    services = []
    for i in cursor.fetchall():
        services.append(i[0])
    sql = "DELETE FROM Addons WHERE ID_SER = %s"  # first delete the addons
    val = (services[0],)
    cursor.execute(sql, val)
    sql = "DELETE FROM Services WHERE ID_SER = %s"
    val = (services[0],)
    cursor.execute(sql, val)
    mydb.commit()


def delete_addon(cursor, mydb, addon):
    """deleting a specific addon"""
    sql = "DELETE FROM Addons WHERE Addon_Name = %s"
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


def get_all_disabled_dates(cursor, mydb, city):
    """this func returns all dates that are disabled for work by the manager
       later, the calendar will read those hours and block them for everyone"""
    # first of all get disabled dates that made by the admin
    cursor.execute("SELECT Day FROM Disabled_Dates;")
    disabled = []
    for i in cursor.fetchall():
        disabled.append(i[0])
    # now we are getting the region of the chosen city
    cursor.execute("SELECT region FROM Cities WHERE City = %s", (city,))
    region = []
    for i in cursor.fetchall():
        region.append(i[0])
    # I added option that if the manager doesnt mind the region, he could use it, and region will be "5"
    if region[0] == 5:
        return disabled
    # here we check on which days there are booking with the area
    cursor.execute("SELECT date FROM Region WHERE area != %s", (region[0],))
    for i in cursor.fetchall():
        disabled.append((i[0]))
    mydb.commit()
    return disabled


def change_hours_for_day(cursor, mydb, start, end, interval):
    """this function will get starting hour, ending hour and the interval between
       and later it will update the time that the customers can choose"""
    sql = "UPDATE Hours SET StartTime = %s, EndTime = %s, SpaceTime = %s"
    val = (start, end, interval)
    cursor.execute(sql, val)
    mydb.commit()


def get_time_for_display(cursor, mydb):
    """this function returns the current starting time, ending time and the interval"""
    cursor.execute("SELECT * FROM Hours;")
    time = []
    for i in cursor.fetchall():
        time.append(i[0])
        time.append(i[1])
        time.append(i[2])
    mydb.commit()
    return time


# def get_hours_for_day(cursor, mydb, day):
#     """get hours for specific day"""
#     hours = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00"]
#     day_hours = []
#     # this is the hours that are taken
#     cursor.execute("SELECT Hour FROM Available_Dates WHERE day_id = %s", (day,))
#     for i in cursor.fetchall():
#         day_hours.append(i[0])
#     for i in day_hours:
#         if i in hours:
#             hours.remove(i)
#     mydb.commit()
#     return hours


def get_hours_for_day(cursor, mydb, day):
    """get hours for specific day"""
    hours = []
    # getting start, end and interval
    time = get_time_for_display(cursor, mydb)
    start_time, end_time, interval = time[0], time[1], time[2]
    hour_start, hour_end = start_time[0:2], end_time[0:2]
    # convert to time object for increasing interval in minutes:
    start_time = datetime.strptime(start_time, '%H:%M')
    temp = str(start_time.time())
    # adding first hour to the list
    hours.append(temp[:-3])
    # this algo is increasing the time by the interval and then updates the old time with the new one
    while hour_end > hour_start:
        # adding th einterval
        time_with_interval = (start_time + timedelta(minutes=interval)).time()
        # converting to string for inserting to list
        temp = str(time_with_interval)
        # to avoid the seconds and get only hours and minutes
        hours.append(temp[:-3])
        # convert the old start time to the new we just added to the list
        start_time = datetime.strptime(hours[-1], '%H:%M')
        # this is to check if we passed the end time:
        hour_start = temp[:2]
    day_hours = []
    # this is the hours that are taken
    cursor.execute("SELECT Hour FROM Available_Dates WHERE day_id = %s", (day,))
    for i in cursor.fetchall():
        day_hours.append(i[0])
    for i in day_hours:
        if i in hours:
            hours.remove(i)
    mydb.commit()
    return hours



def get_all_cities(cursor, mydb):
    """this func gets all cities and sort them alphabet"""
    cursor.execute("SELECT City FROM Cities;")
    # will hold all the cities there are inside DB
    cities = []
    fetched_data = cursor.fetchall()
    for city in fetched_data:
        cities.append(city[0])
    sorting_list = sorted(cities)
    mydb.commit()
    return sorting_list


def add_city(cursor, mydb, city, region):
    """will add city to the DB"""
    print(region)
    sql = "INSERT INTO Cities (City, region) VALUES (%s, %s)"
    val = (city, region, )
    cursor.execute(sql, val)
    mydb.commit()


def delete_city(cursor, mydb, city):
    "will delete city from DB"
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


def get_description_for_service(cursor, mydb, service):
    """will change description for service"""
    sql = "SELECT Service_Description FROM Services WHERE Service_Name = %s"
    val = (service, )
    cursor.execute(sql, val)
    description = []
    for i in cursor.fetchall():
        description.append(i[0])
    mydb.commit()
    if description == []:
        description = "אין תיאור כרגע"
        return description
    else:
        return description[0]


def edit_addon_price(cursor, mydb, price, addon):
    """this func gets addon name and update his price"""
    sql = "UPDATE Addons SET Addon_Price = %s WHERE Addon_Name = %s"
    val = (price, addon)
    cursor.execute(sql, val)
    mydb.commit()


# def get_values(cursor, mydb, values):
#     """will get all values from the booking and add it to DB"""
#     hold_data = {}
#     hold_data["full_name"] = values["fullName"]
#     hold_data["email"] = values["email"]
#     hold_data["phone"] = values["phone"]
#     hold_data["address"] = values["fullAddress"]
#     hold_data["service"] = values["service"] + " " + values["addons"]
#     hold_data["date"] = day_plus_one(values["date"].split("T")[0])
#     hold_data["hour"] = values["hour"]
#     hold_data["price"] = values["price"]
#     hold_data["comments"] = values["comments"]
#     add_new_booking(cursor, mydb, hold_data)


# def add_new_booking(cursor, mydb, data):
#     """will add the booking details to "Customers" table in DB"""
#     sql = "INSERT INTO Customers (Full_Name, Email, Phone, Address, Service, Date, Hour, Price, Comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     val = (data["full_name"], data["email"], data["phone"], data["address"], data["service"], data["date"], data["hour"], data["price"], data["comments"], )
#     cursor.execute(sql, val)
#     mydb.commit()


def add_new_booking(cursor, mydb, data):
    """will add the booking details to "Customers" table in DB"""
    full_service = data["service"] + " " + data["addons"]
    # the date the comes is 1 day earlier so i'm moving it 1 day forward
    new_date = day_plus_one(data["date"].split("T")[0])
    sql = "INSERT INTO Customers (Full_Name, Email, Phone, Address, Service, Date, Hour, Price, Comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (data["fullName"], data["email"], data["phone"], data["fullAddress"], full_service, new_date, data["hour"], data["price"], data["comments"], )
    cursor.execute(sql, val)
    add_to_region(cursor, mydb, data["cit"], new_date)
    # mydb.commit()


def add_to_region(cursor, mydb, city, dat):
    # getting the region of a city
    cursor.execute("SELECT region FROM Cities WHERE City = %s", (city,))
    region = []
    for i in cursor.fetchall():
        region.append(i[0])
    # after we know the region, we insert the data into "Region" table with the date for later use
    sql = "INSERT INTO Region (area, date) VALUES (%s, %s)"
    val = (region[0], dat, )
    cursor.execute(sql, val)
    mydb.commit()


def get_all_customers(cursor, mydb):
    """get all customers details from db for displaying in the table"""
    cursor.execute("SELECT * FROM Customers;")
    customers = []
    today = date.today()
    future_bookings = []
    for i in cursor.fetchall():
        customers.append(list(i))
    mydb.commit()
    sorted_by_date = sorted(customers, key=lambda x: x[6])
    for i in sorted_by_date:
        if i[6] >= str(today):
            future_bookings.append(i)
    return future_bookings


def get_customers_address(cursor, mydb):
    """get all customers details from db for displaying in the table
       the showing addresses will be only the future bookings"""
    cursor.execute("SELECT Address FROM Customers;")
    address = []
    final_results = []
    for i in cursor.fetchall():
        address.append(list(i))
    mydb.commit()
    cursor.execute("SELECT * FROM Customers;")
    customers = []
    today = date.today()
    future_bookings = []
    for i in cursor.fetchall():
        customers.append(list(i))
    mydb.commit()
    # this is sorting the list by the date
    sorted_by_date = sorted(customers, key=lambda x: x[6])
    # this loop keeping only the futre bookings after today
    for i in sorted_by_date:
        if i[6] >= str(today):
            future_bookings.append(i[4])
    # after we have only future bookings, we are getting only the addresses for displaying in map
    for i in address:
        if i[0] in future_bookings:
            # whatever inside "future_bookings" is a future bookings so we append it to "final_results"
            final_results.append(i)
    return final_results

# def get_customers_address(cursor, mydb):
#     """get all customers details from db for displaying in the table"""
#     cursor.execute("SELECT * FROM Customers;")
#     address = []
#     for i in cursor.fetchall():
#         # print(i[4])
#         address.append(list(i[4]))
#     mydb.commit()
#     # sorted_by_date = sorted(customers, key=lambda x: x[6])
#     return address

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


def add_main_img_to_service(cursor, mydb, service, img):
    """this func adds the main image to certain seervice"""
    sql = "UPDATE Services SET Service_Image = %s WHERE ID_SER = %s"
    val = (img, service)
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


def get_note(cursor, mydb, service):
    note = []
    cursor.execute("SELECT Note FROM Services WHERE ID_SER = %s", (service,))
    for i in cursor.fetchall():
        note.append(i[0])
    mydb.commit()
    return note


def edit_service_name(cursor, mydb, service, new_name):
    """this func changes service name from the admin's panel"""
    # sql = "UPDATE Addons, Services SET Addons.ID_SER = %s, Services.ID_SER = %s, Services.Service_Name = %s " \
    #       "FROM Addons addon, Services ser WHERE addon.ID_SER = %s AND ser.ID_SER = %s"
    # val = (new_name, new_name, new_name, service, service)
    # cursor.execute(sql, val)
    # mydb.commit()
    # sql = "UPDATE Addons SET ID_SER = %s WHERE ID_SER = %s"
    # val = (new_name, service)
    # cursor.execute(sql, val)
    # mydb.commit()
    sql = "UPDATE Services SET Service_Name = %s WHERE Service_Name = %s"
    val = (new_name, service)
    cursor.execute(sql, val)
    mydb.commit()


def disable_by_region(cursor, mydb, city):
    cursor.execute("SELECT Address FROM Customers;")
    address = []
    final_results = []
    for i in cursor.fetchall():
        address.append(list(i))
    # sorted_by_date = sorted(customers, key=lambda x: x[6])


if __name__ == '__main__':
    cursor, connection = connect_db()  # connect to DB
    # get_hours_for_day(cursor, connection)
