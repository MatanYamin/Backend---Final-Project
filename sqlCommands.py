import pymysql
import connect_database as con

# database connection

# queries for retrievint all rows
# retrive = "Select notes from ea_appointments;"


def connect_db():
    """need to run few edge tests
    checked some thing"""
    connection = con.connect_db()
    cursor = connection.cursor()
    return cursor, connection


def select_db(query):
    """this function needs to retrieve something from DB
         it will retrieve whatever we want as long we define it first
         still has some changes to make
         note to myself: add all options that is needed!
         checked somethings"""
    this_query = ""
    rows = ""
    if query == "*":
      # incase we want all (for tests),
      # ***still need to have some tests
      this_query += "Select notes from ea_appointments;"
      cursor.execute(this_query)
      rows += cursor.fetchall()
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


    return rows

#commiting the connection then closing it.
# connection.commit()
# connection.close()


if __name__ == '__main__':
    # connection = con.connect_db()
    # cursor = connection.cursor()
    cursor, connection = connect_db()
    datas = select_db("dates")
    for i in datas:
        print(i)

    connection.commit()
    connection.close()
    # executing the quires
    # cursor.execute(retrive)
    # data = cursor.fetchall()
    # for row in data:
    #     print(row)
