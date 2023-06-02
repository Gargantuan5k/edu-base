import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="edubase",
    port=3307  # TODO KEEP THIS COMMENTED unless reqd
    )
cursor = db.cursor()

table = 'students_src'
roll_no = 3
name = 'Stu3'

q = "select roll_no, name from students_src"
cursor.execute(q)
res = cursor.fetchone()
print(res is not None)

cursor.execute('delete from students_src')
cursor.execute(q)
res = cursor.fetchone()
print(res is not None)

cursor.execute("insert into students_src values(2, 'Stu2')")
cursor.execute(q)
res = cursor.fetchone()
print(res is not None)

db.commit()
cursor.close()
db.close()