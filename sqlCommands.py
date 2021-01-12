import pymysql
import connect_database as connect
import synCalendar as sync


def connect_db():
    """connects to DB"""
    connection = connect.connect_db()
    cursor = connection.cursor()
    return cursor, connection


def get_last_event():
    """still need to add a loop that runs all the time"""
    data_list = []
    query = "SELECT * FROM ea_appointments ORDER BY ID DESC LIMIT 1;"
    second_query ="SELECT * FROM ea_users ORDER BY ID DESC LIMIT 1;"
    third_query = "SELECT name FROM ea_services ORDER BY ID DESC LIMIT 1;"
    # ********************** check that id is matching! ************************* #
    cursor.execute(query)
    times_and_note = cursor.fetchall()
    data_list.append(times_and_note)
    cursor.execute(second_query)
    user_details = cursor.fetchall()
    data_list.append(user_details)
    cursor.execute(third_query)
    service = cursor.fetchall()
    data_list.append(service)
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
    elif query == "email":
      this_query += "Select email from ea_appointments;"
      cursor.execute(this_query)
      rows += cursor.fetchall()
    elif query == "start":
        this_query += "Select start_datetime from ea_appointments;"
        cursor.execute(this_query)
        rows += cursor.fetchall()
    elif query == "end":
        this_query += "Select end_datetime from ea_appointments;"
        cursor.execute(this_query)
        rows += cursor.fetchall()
    elif query == "address":
        this_query += "Select address from ea_appointments;"
        cursor.execute(this_query)
        rows += cursor.fetchall()
        this_query += "Select city from ea_appointments;"
        cursor.execute(this_query)
        rows += cursor.fetchall()
    return rows


def get_event_data(event):
    list_of_items = []
    dict = {}
    for i in event:
        for j in i:
            for k in j:
                list_of_items.append(k)
    dict["start_time"] = list_of_items[2].isoformat()
    dict["end_time"] = list_of_items[3].isoformat()
    dict["note"] = list_of_items[4]
    dict["first_name"] = list_of_items[12]
    dict["family_name"] = list_of_items[13]
    dict["email"] = list_of_items[14]
    dict["phone"] = list_of_items[16]
    dict["street"] = list_of_items[17]
    dict["city"] = list_of_items[18]
    dict["zip_code"] = list_of_items[20]
    dict["full_address"] = dict["street"] + ', ' + dict["city"] + ', ' + dict["zip_code"]
    dict["summary"] = "ניקוי עם סקיי-קלינר!"
    return dict


def create_and_insert(service, data):

    event = {
        'summary': data["summary"],
        'location': data["full_address"],
        'description': "ניקיון של סקיי קלינר ספות",
        'start': {
            'dateTime': data["start_time"],
            'timeZone': 'Asia/Jerusalem',
        },
        'end': {
            'dateTime': data["end_time"],
            'timeZone': 'Asia/Jerusalem',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
        ],
        'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    cursor, connection = connect_db()  # connect to DB
    new_event = get_last_event()  # getting the last event
    data = get_event_data(new_event)  # get dictionary for all event params
    service = sync.syncalendar_adn_service(True)  # get the "writing" service from synCalendar
    create_and_insert(service, data)  # creating event in inserting it to calendar
    # closing connection after the connect
    connection.commit()
    connection.close()

