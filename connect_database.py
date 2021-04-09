# Programmed by Matan Yamin - Final Project.
import mysql.connector as mysql
import config as cn


def connect_db():
    # enter your server IP address/domain name
    host_ip = cn.db_ip()  # "3.138.43.76"
    # database name I want to connect to
    database = cn.db_name()
    # this is the user name I created
    user_name = cn.db_user_name()
    # user password
    password = cn.db_pass()
    # connect to MySQL server
    db_connection = mysql.connect(host=host_ip, database=database, user=user_name, password=password, port=3306)
    return db_connection
    # connect confirmation
    # print("Connected to:", db_connection.get_server_info())


if __name__ == '__main__':
    connect_db()
