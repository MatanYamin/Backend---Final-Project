# Backend---Final-Project
<img src="https://i.ibb.co/WnBBRwt/Sky-cleaner-backend.png" height="190" width="320">
This part focuses on the beckend side of Sky Cleaner Apoointment system web site, bulid by Matan Yamin.

On this part of the project, there will be designs of the system backend, after schedualing an appointment.

This code will be easy to read and to understand, and mostly, will be efficient for it's pruposes.

This part has been written with Python 3.7 via pycharm and using libraries.

The backend part has to handle with many features as:

Connecting DB via "connect_db.py".
the DB is sitting on AWS servers.

Synchronising CEO's calendar with google API and let writing and reading permissions with "synCalendar.py"

With "db_handling.py" we will -
Constantly get updates from DB and verify new appointment.
Add new event to CEO calendar and customer calendar.
send Email to customer.
Let CEO decide about availabilty from his calendar
Manually able to add an appointment
SMS sending
and more features to come

