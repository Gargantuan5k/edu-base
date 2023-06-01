import mysql.connector
import frontend


def init_db():
    # Establish a connection to the MySQL database
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="edubase",
    # port=3307  # KEEP THIS COMMENTED unless reqd
    )
    cursor = db.cursor()

    return db, cursor

# Adding date column to attendance
def mysql_query_1():
    # Initialise DB and create cursor
    db, cursor = init_db()

    # Check if the date column already exists in the table
    check_query = f"SHOW COLUMNS FROM attendance LIKE '{frontend.tdy_date}'"
    cursor.execute(check_query)
    result = cursor.fetchone()

    # Add the date as column to the table if it doesn't already exist
    if result is None:
        alter_query = f"ALTER TABLE attendance ADD COLUMN `{frontend.tdy_date}` varchar(20)"
        cursor.execute(alter_query)

    # Commit the changes to the database
    db.commit()
    # Close the cursor and database connection
    cursor.close()
    db.close()

# Getting name to add attendance of
def mysql_query_2():
    # Initialise DB and create cursor
    db, cursor = init_db()

    getName_query = f"SELECT name FROM attendance WHERE roll_no = {frontend.rNo}"
    cursor.execute(getName_query)
    getName = cursor.fetchone()
    print("Enter attendance for "+getName[0])
    # Commit the changes to the database
    db.commit()
    # Close the cursor and database connection
    cursor.close()
    db.close()

# Adding student attendance
def mysql_query_3():
    # Initialise DB and create cursor
    db, cursor = init_db()

    # Adding attendance of student
    attendance_query = f"UPDATE attendance SET `{frontend.tdy_date}` = '{frontend.markedAttendance}' WHERE roll_no = {frontend.rNo}"
    cursor.execute(attendance_query)

    # Commit the changes to the database
    db.commit()

    # Close the cursor and database connection
    cursor.close()
    db.close()

# Adding student to table
def mysql_query_4():
    # Initialise DB and create cursor
    db, cursor = init_db()

    # Adding data to table
    addStudent_query = f"INSERT INTO `{frontend.table}`(roll_no, name) values('{frontend.rNo}', '{frontend.Name}')"
    cursor.execute(addStudent_query)

    print("New student added!")
    # Commit the changes to the database
    db.commit()
    # Close the cursor and database connection
    cursor.close()
    db.close()

# Getting name to remove from table
def mysql_query_5():
    # Initialise DB and create cursor
    db, cursor = init_db()

    getName_query = f"SELECT name FROM `{frontend.table}` WHERE roll_no = '{frontend.rNo}'"
    cursor.execute(getName_query)
    getName = cursor.fetchone()
    print("Are you sure you want to remove "+getName[0])

    # Commit the changes to the database
    db.commit()
    # Close the cursor and database connection
    cursor.close()
    db.close()

# Removing student from table
def mysql_query_6():
    # Initialise DB and create cursor
    db, cursor = init_db()

    # Removing student from table
    removeStudent_query = f"DELETE FROM `{frontend.table}` WHERE roll_no = '{frontend.rNo}'"
    cursor.execute(removeStudent_query)
    
    # Commit the changes to the database
    db.commit()
    # Close the cursor and database connection
    cursor.close()
    db.close()
