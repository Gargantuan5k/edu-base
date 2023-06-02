import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="edubase",
    port=3307  # TODO KEEP THIS COMMENTED unless reqd
    )

def get_cursor():
    # Establish a connection to the MySQL database
    cursor = db.cursor()
    return cursor

def close_db():
    db.close()

def check_src_exists():
    cursor = get_cursor()
    query = f"select roll_no, name from students_src"
    cursor.execute(query)
    res = cursor.fetchall()

    cursor.close()
    return res is not None


def check_student_rec_exists(roll):
    cursor = get_cursor()
    query = f"select name from students_src where roll_no = '{roll}'"
    cursor.execute(query)
    res = cursor.fetchall()

    cursor.close()
    return bool(res)


def create_list(**kwargs):
    cursor = get_cursor()
    
    if check_src_exists():
        cursor.execute('delete from students_src')

    students = kwargs['stu_dict']

    for roll_no, name in students.items():
        query = f"insert into students_src(roll_no, name) values('{roll_no}', '{name}')"
        cursor.execute(query)
    
    db.commit()
    cursor.close()


def add_student(roll_no, name, exists=False):
    cursor = get_cursor()

    if exists:
        cursor.execute(f"delete from students_src where roll_no = '{roll_no}'")
    
    add_query = f"insert into students_src(roll_no, name) values('{roll_no}', '{name}')"
    cursor.execute(add_query)

    db.commit()
    cursor.close()
    return (roll_no, name)


def delete_student(roll_no):
    cursor = get_cursor()

    exists_query = f"select * from students_src where roll_no = '{roll_no}'"
    cursor.execute(exists_query)
    res = cursor.fetchall()
    if not res:
        return False
    
    get_query = f"select * from students_src where roll_no = '{roll_no}'"
    cursor.execute(get_query)
    res = cursor.fetchall()
    del_query = f"delete from students_src where roll_no = '{roll_no}'"    
    cursor.execute(del_query)

    db.commit()
    cursor.close()
    return res


def update_student(roll_no, new_name):
    cursor = get_cursor()
    res = {}

    get_orig_query = f"select * from students_src where roll_no = '{roll_no}'"
    cursor.execute(get_orig_query)
    orig = cursor.fetchall()
    res['original'] = orig

    update_query = f"update students_src set name = '{new_name}' where roll_no = '{roll_no}'"
    cursor.execute(update_query)
    res['new'] = (roll_no, new_name)

    db.commit()
    cursor.close()
    return res

def add_date(tdy_date):
    cursor = get_cursor()

    # Check if the date column already exists in the table
    check_query = f"SHOW COLUMNS FROM attendance LIKE '{tdy_date}'"
    cursor.execute(check_query)
    result = cursor.fetchall()

    # Add the date as column to the table if it doesn't already exist
    if result is None:
        alter_query = f"ALTER TABLE attendance ADD COLUMN `{tdy_date}` varchar(20)"
        cursor.execute(alter_query)

    db.commit()
    cursor.close()


def get_name(r_no):
    cursor = get_cursor()

    # Get student name, give prompt for att
    getName_query = f"SELECT name FROM attendance WHERE roll_no = {r_no}"
    cursor.execute(getName_query)
    getName = cursor.fetchall()
    print("Enter attendance for " + getName[0])

    db.commit()
    cursor.close()


def mark_att(tdy_date, att, r_no):
    cursor = get_cursor()

    # Adding attendance of student
    attendance_query = f"UPDATE attendance SET `{tdy_date}` = '{att}' WHERE roll_no = {r_no}"
    cursor.execute(attendance_query)

    db.commit()
    cursor.close()
