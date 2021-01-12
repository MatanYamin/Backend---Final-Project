import pymysql
import connect_database as con
import httplib2
import os

from apiclient import discovery



# database connection

# queries for retrievint all rows
# retrive = "Select notes from ea_appointments;"


def connect_db():
    """need to run few edge tests
    checked some thing"""
    connection = con.connect_db()
    cursor = connection.cursor()
    return cursor, connection


def get_last_query():
    data_list = []
    # times_and_note = []
    # user_details = []
    query = "SELECT * FROM ea_appointments ORDER BY ID DESC LIMIT 1;"
    second_query ="SELECT * FROM ea_users ORDER BY ID DESC LIMIT 1;"
    third_query = "SELECT name FROM ea_services ORDER BY ID DESC LIMIT 1;"
    cursor.execute(query)
    times_and_note = cursor.fetchall()
    data_list.append(times_and_note)
    cursor.execute(second_query)
    user_details = cursor.fetchall()
    data_list.append(user_details)
    cursor.execute(third_query)
    service = cursor.fetchall()
    data_list.append(service)
    # return times_and_note, user_details
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
      # incase we want all (for tests),
      # ***still need to have some tests
      this_query += "Select * from ea_appointments;"
      get_id = "Select id from "
      cursor.execute(this_query)
      # print(cursor.fetchall())
      rows += cursor.fetchall()
      id.append()
    elif query == "dates":
        # incase we want only dates,
        # ***still need to have some tests"""
      this_query += "Select notes from ea_appointments;"
      cursor.execute(this_query)
      rows += cursor.fetchall()
    elif query == "email":
      # incase we want only emails,
      # ***still need to have some tests"""
      this_query += "Select notes from ea_appointments;"
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


    return rows

#commiting the connection then closing it.
# connection.commit()
# connection.close()


def create_event(data):
    list_of_items = []
    for i in data:
        for j in i:
            for k in j:
                list_of_items.append(k)
    print(list_of_items)
    # print(list_of_items)
    id = list_of_items[8]
    made_appointment_time = list_of_items[1]
    start_time = list_of_items[2]
    end_time = list_of_items[3]
    note = list_of_items[4]
    first_name = list_of_items[12]
    family_name = list_of_items[13]
    email = list_of_items[14]
    phone = list_of_items[16]
    street = list_of_items[17]
    city = list_of_items[18]
    zip_code = list_of_items[20]
    service = list_of_items[-1]
    print("made_appointment_time", made_appointment_time)
    print("start_time", start_time)
    print("end_time", end_time)
    print("note", note)
    print("id", id)
    print("first_name", first_name)
    print("family_name", family_name)
    print("mail", email)
    print("phone", phone)
    print("street", street)
    print("city", city)
    print("zip_code", zip_code)
    print("service", service)
    full_address = street + ',' + city + ',' + zip_code
    summary = "ניקוי עם סקייקלינר!"
    event = {
        'summary': summary,
        'location': full_address,
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [
            {'email': email},
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
    cursor, connection = connect_db()
    retrieve_from_db = select_db("end")
    # for line in retrieve_from_db:
    #     print(line[0])
    data = get_last_query()
    create_event(data)
    connection.commit()
    connection.close()  # closing connection after the connect

