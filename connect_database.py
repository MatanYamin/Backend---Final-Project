import mysql.connector as mysql

# enter your server IP address/domain name
HOST = "3.138.43.76"  # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "skycleaner"
# this is the user you create
USER = "matanym"
# user password
PASSWORD = "Password"
# connect to MySQL server
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=3306)
print("Connected to:", db_connection.get_server_info())
# enter your code here!