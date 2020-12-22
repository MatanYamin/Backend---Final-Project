import pymysql
import connect_database as con


# database connection
connection = con.connect_db()
cursor = connection.cursor()

# queries for retrievint all rows
retrive = "Select notes from ea_appointments;"

def select_db(query):
    """this function needs to retrieve something from DB
         it will retrieve whatever we want as long we define it first
         still has some changes to make"""
    this_query = ""
    rows = ""
    if query == "*":
      this_query += "Select notes from ea_appointments;"
      cursor.execute(this_query)
      rows += cursor.fetchall()
    elif query == "dates":
      this_query += "Select notes from ea_appointments;"
      cursor.execute(this_query)
      rows += cursor.fetchall()
    elif query == "email":
      this_query += "Select notes from ea_appointments;"
      cursor.execute(this_query)
      rows += cursor.fetchall()

    return rows

datas = select_db("dates")
for i in datas:
   print(i)
#executing the quires
cursor.execute(retrive)
data = cursor.fetchall()
for row in data:
   print(row)


#commiting the connection then closing it.
connection.commit()
connection.close()