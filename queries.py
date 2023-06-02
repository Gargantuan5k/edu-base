import mysql.connector


def init_db():
    # Establish a connection to the MySQL database
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="edubase",
    port=3307  # TODO KEEP THIS COMMENTED unless reqd
    )
    cursor = db.cursor()

    return db, cursor


def check_students_exists():
    _, cursor = init_db()
    query = f"select roll_no, name from students_src"
    cursor.execute(query)
    res = cursor.fetchone()
    return res is not None


def add_students(**kwargs):
    db, cursor = init_db()
    
    if check_students_exists():
        cursor.execute('delete from students_src')

    students = kwargs['stu_dict']

    for roll_no, name in students.items():
        query = f"insert into students_src(roll_no, name) values('{roll_no}', '{name}')"
        cursor.execute(query)
    
    db.commit()
    cursor.close()
    db.close()


def add_date(tdy_date):
    db, cursor = init_db()

    # Check if the date column already exists in the table
    check_query = f"SHOW COLUMNS FROM attendance LIKE '{tdy_date}'"
    cursor.execute(check_query)
    result = cursor.fetchone()

    # Add the date as column to the table if it doesn't already exist
    if result is None:
        alter_query = f"ALTER TABLE attendance ADD COLUMN `{tdy_date}` varchar(20)"
        cursor.execute(alter_query)

    db.commit()
    cursor.close()
    db.close()


def get_name(r_no):
    db, cursor = init_db()

    # Get student name, give prompt for att
    getName_query = f"SELECT name FROM attendance WHERE roll_no = {r_no}"
    cursor.execute(getName_query)
    getName = cursor.fetchone()
    print("Enter attendance for " + getName[0])

    db.commit()
    cursor.close()
    db.close()


def mark_att(tdy_date, att, r_no):
    db, cursor = init_db()

    # Adding attendance of student
    attendance_query = f"UPDATE attendance SET `{tdy_date}` = '{att}' WHERE roll_no = {r_no}"
    cursor.execute(attendance_query)

    db.commit()
    cursor.close()
    db.close()
