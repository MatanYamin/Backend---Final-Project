import mysql.connector as mysql


def connect_db():
    # enter your server IP address/domain name
    host_ip = '3.138.43.76'  # "3.138.43.76"
    # database name I want to connect to
    database = "skycleaner"
    # this is the user name I created
    user_name = "matanym"
    # user password
    password = "Password"
    # connect to MySQL server
    db_connection = mysql.connect(host=host_ip, database=database, user=user_name, password=password, port=3306)
    return db_connection
    print("Connected to:", db_connection.get_server_info())


if __name__ == '__main__':
    connect_db()
