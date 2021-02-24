# Programmed by Matan Yamin - Final Project.
import connect_database as connect
import synCalendar as sync
import email_handler as email
import datetime
from time import strftime
import threading
BOOKING_LIST = []  # read from...


def connect_db():
    """connects to DB, here wer'e connecting to DB using 'connect_database'
    and ther returning the connection inorder to fetch data"""
    connection = connect.connect_db()
    cursor = connection.cursor()
    return cursor, connection


def verify_customer(data_event):
    """check if the id of appointment details are match to customer details
    if not, find the right one"""
    list_event = []
    new_event = []
    # thi loops is fetching the data from db
    for i in data_event:
        for j in i:
            for k in j:
                list_event.append(k)
    id1 = list_event[8]
    id2 = list_event[11]
    if id1 == id2:
        return data_event
    # in else that means that we need to match the appointment to the same person
    else:
        query = "SELECT * FROM ea_appointments  ORDER BY ID DESC LIMIT 1;"
        cursor.execute(query)
        times_and_note = cursor.fetchall()
        new_event.append(times_and_note)
        # second_query = "SELECT * FROM ea_users WHERE ID = ? LIMIT 1;"
        cursor.execute("SELECT * FROM ea_users WHERE ID = %s LIMIT 1", (id1,))
        user_details = cursor.fetchall()
        new_event.append(user_details)
        service_details = get_service_by_id(new_event[0][0][9])
        # third_query = "SELECT name FROM ea_services ORDER BY ID DESC LIMIT 1;"
        # cursor.execute(third_query)
        # service = cursor.fetchall()
        new_event.append(service_details)
        return new_event


def insert_data_list(query, data_list):
    """get query and retrieve data with that query from db"""
    cursor.execute(query)
    data_to_fetch = cursor.fetchall()
    data_list.append(data_to_fetch)
    return data_list


def get_service_by_id(id):
    """here were getting the kind of service that the customer chose to use"""
    cursor.execute("SELECT * FROM ea_services WHERE ID = %s LIMIT 1", (id,))
    service_details = cursor.fetchall()
    return service_details


def get_last_event():
    """still need to add a loop that runs all the time"""
    data_list = []
    query = "SELECT * FROM ea_appointments  ORDER BY ID DESC LIMIT 1;"
    insert_data_list(query, data_list)
    second_query ="SELECT * FROM ea_users ORDER BY ID DESC LIMIT 1;"
    insert_data_list(second_query, data_list)
    service_details = get_service_by_id(data_list[0][0][9])
    # third_query = "SELECT name FROM ea_services ORDER BY ID DESC LIMIT 1;"
    # data_list = insert_data_list(third_query, data_list)
    data_list.append(service_details)
    data_list = verify_customer(data_list)
    return data_list


def select_db(query):
    """this function needs to retrieve something from DB
         it will retrieve whatever we want as long we define it first
         still has some changes to make
         note to myself: add all options that is needed!
         checked somethings"""
    this_query = ""
    rows = []
    id = []
    if query == "all":
      this_query += "Select * from ea_appointments;"
      cursor.execute(this_query)
      rows += cursor.fetchall()
      id.append()
    # if we only want email
    elif query == "email":
      this_query += "Select email from ea_appointments;"
      cursor.execute(this_query)
      rows += cursor.fetchall()
    # if we only want start date
    elif query == "start":
        this_query += "Select start_datetime from ea_appointments;"
        cursor.execute(this_query)
        rows += cursor.fetchall()
    # if we only want end date
    elif query == "end":
        this_query += "Select end_datetime from ea_appointments;"
        cursor.execute(this_query)
        rows += cursor.fetchall()
    # if we only want address (getting street and city address)
    elif query == "address":
        this_query += "Select address from ea_appointments;"
        cursor.execute(this_query)
        rows += cursor.fetchall()
        this_query += "Select city from ea_appointments;"
        cursor.execute(this_query)
        rows += cursor.fetchall()
    return rows


def get_day(date_list):
    """this function is used to get the exact day in week using strftime"""
    splitted_dates = date_list.strftime("%d/%m/%Y %H:%M:%S").split(" ")
    date = splitted_dates[0].split("/")
    d = int(date[0])
    m = int(date[1])
    if m < 10:
        m = m%10
    y = int(date[2])
    day = datetime.datetime(y, m, d).strftime('%A')
    # here were translating the day to hebrew
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


def get_event_data(event):
    """get event data and insert to dictionary
    with the right key values, later we will use it for event, email and other
    purposes"""
    list_of_items = []
    dict = {}
    # loop to get data
    for i in event:
        for j in i:
            for k in j:
                list_of_items.append(k)
    # get the current day of the date
    dict["day"] = get_day(list_of_items[2])
    split_time = list_of_items[2].strftime("%d/%m/%y %H:%M").split(" ")
    dict["number date"] = split_time[0]  # appointment time
    dict["time"] = split_time[1]  #
    dict["start time"] = list_of_items[2].isoformat()
    dict["end time"] = list_of_items[3].isoformat()
    dict["note"] = list_of_items[4]
    dict["first name"] = list_of_items[12]
    dict["family name"] = list_of_items[13]
    dict["full name"] = dict["first name"] + " " + dict["family name"]
    dict["email"] = list_of_items[14]
    dict["phone"] = list_of_items[16]
    dict["street"] = list_of_items[17]
    dict["city"] = list_of_items[18]
    dict["call me"] = list_of_items[20]
    dict["service"] = list_of_items[24]
    dict["price"] = str(list_of_items[26]) + " ₪"
    dict["admin email"] = "matanyamin01@gmail.com"
    dict["full address"] = dict["street"] + ', ' + dict["city"]
    dict["summary"] = "ניקוי עם סקאי קלינר!"
    return dict


def create_and_insert(service, data):
    """we get here data after inserting to dictionary all parameters
    creating the event to send to the relevant places"""
    event = {  # this event will go the manager and customer calendar in phone
        'summary': data["summary"],
        'location': data["full address"],
        'description': "ניקיון של סקיי קלינר ספות",
        'start': {
            'dateTime': data["start time"],
            'timeZone': 'Asia/Jerusalem',
        },
        'end': {
            'dateTime': data["end time"],
            'timeZone': 'Asia/Jerusalem',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
        ],
        'attendees': [
            {'email': data["email"]},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 24 * 60},
            ],
        },
    }
    # connecting to calendar and insert event
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    email.email_handle(data)


def get_hash():
    """this func is used to verify if the data from DB is new or already there"""

    connection.commit()
    query = "SELECT hash FROM ea_appointments ORDER BY ID DESC LIMIT 1;"
    cursor.execute(query)
    hash_to_fetch = cursor.fetchall()
    return hash_to_fetch


def check_for_update():
    """check for new bookings with hash code that we have in the table.
    if we have that code already, means we dont have any new booking.
    Do that constantly."""

    cursor, connection = connect_db()  # connect to DB
    hash_code = get_hash()
    # print(hash_code)
    if hash_code in BOOKING_LIST:
        # print("this is the hash-> ", hash_code)
        # print("this is the list-> ", BOOKING_LIST)
        return False
    BOOKING_LIST.append(hash_code)
    connection.commit()
    connection.close()
    return True


def main_run():
    """here is the function that start all functions"""
    threading.Timer(4.0, main_run).start()
    if check_for_update():
        print("new booking!")
        # cursor, connection = connect_db()  # connect to DB
        new_event = get_last_event()  # getting the last event
        data = get_event_data(new_event)  # get dictionary for all event params
        service = sync.syncalendar_and_service()  # get the "writing" service from synCalendar
        create_and_insert(service, data)  # creating event in inserting it to calendar
        # closing connection after the connect
        # connection.commit()
        # connection.close()
    # else:
    #     print("NO new booking")


if __name__ == '__main__':
    cursor, connection = connect_db()  # connect to DB
    main_run()

