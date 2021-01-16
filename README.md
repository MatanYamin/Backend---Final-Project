# Backend---Final-Project
<img src="https://i.ibb.co/WnBBRwt/Sky-cleaner-backend.png" height="190" width="320">
This part focuses on the beckend side of Sky Cleaner Apoointment system web site, bulid by Matan Yamin.

On this part of the project, there will be designs of the system backend, after schedualing an appointment.

This code will be easy to read and to understand, and mostly, will be efficient for it's pruposes. &#8987; <br>

This part has been written with Python 3.7 via pycharm and using libraries. &#128013; <br>

The backend part has to handle with many features as:

Connecting DB with connect_db.py &#9989; <br>

the DB is sitting on AWS servers. &#9989; <br>

Synchronising CEO's calendar with google API and let writing and reading permissions with "synCalendar.py" &#9989; <br>

With "db_handling.py" we will -<br><br>
&#8226; Constantly get updates from DB and verify new appointment.<br>
&#8226; Check with hash code about new bookings.<br>
&#8226; Google synchronization: add new event to admin's calendar and customer's calendar with book details.<br>
&#8226; Send confirmation Email to customer.<br>
&#8226; Send new booking details Email to manager.<br>
&#8226; Let CEO decide about availabilty from his calendar.<br>
&#8226; Manually able to add an appointment.<br>
&#8226; SMS sending. <br>
&#8226; Booking Cancelation. <br>
&#8226; Reminders. <br>
&#8226; Run on PM2 instantly. <br>


and more features to come.

