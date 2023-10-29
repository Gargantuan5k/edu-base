import mysql.connector
import src_queries
import csv
from os import getcwd, path as ospath

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="edubase",
    port=3307  # TODO KEEP THIS COMMENTED unless reqd
    )

def get_cursor(dictionary=False):
    # Establish a connection to the MySQL database
    cursor = db.cursor(dictionary=dictionary)
    return cursor

def populate():
    cursor = get_cursor()
    q = f"insert into attendance(roll_no, name) select roll_no, name from students_src where roll_no not in (select roll_no from attendance)"
    cursor.execute(q)
    db.commit()
    cursor.close()

def check_date_exists(tdy_date):
    cursor = get_cursor()

    check_query = f"SHOW COLUMNS FROM attendance LIKE '{tdy_date}'"
    cursor.execute(check_query)
    result = cursor.fetchall()
    cursor.close()

    return bool(result)

def prepare_table(tdy_date):
    ex = src_queries.check_src_exists()
    if not ex: return False

    cursor = get_cursor()
    populate()

    # Check if the date column already exists in the table
    result = check_date_exists(tdy_date)

    # Add the date as column to the table if it doesn't already exist
    if not result:
        alter_query = f"ALTER TABLE attendance ADD COLUMN `{tdy_date}` varchar(20)"
        cursor.execute(alter_query)

    db.commit()
    cursor.close()
    return True

def check_unmarked(tdy_date): # @returns bool<any unmarked att?>, bool<all att unmarked?>, list[tuple[str<stu_roll>, str<stu_name>]] x2
    cursor = get_cursor()
    q1 = f"select roll_no, name from attendance where `{tdy_date}` is NULL"
    q2 = f"select roll_no, name from attendance"

    cursor.execute(q1)
    unm = cursor.fetchall()
    cursor.execute(q2)
    total = cursor.fetchall()
    cursor.close()

    return bool(unm), (len(unm) == len(total)), unm, total

def mark_attendance(tdy_date, present, absent):
    cursor = get_cursor()
    for rno in present:
        q = f"update attendance set `{tdy_date}` = 'p' where roll_no = '{rno}'"
        cursor.execute(q)
    for rno in absent:
        q = f"update attendance set `{tdy_date}` = 'a' where roll_no = '{rno}'"
        cursor.execute(q)
    db.commit()
    cursor.close()


def wipe_attendance(tdy_date):
    cursor = get_cursor()
    wipe_q = f"update attendance set `{tdy_date}` = NULL where roll_no is not NULL"
    cursor.execute(wipe_q)
    db.commit()
    cursor.close()


def view(mode, path=None):
    dict_cursor = get_cursor(dictionary=True)
    text_cursor = get_cursor()
    q = 'select * from attendance'

    if mode == 'terminal':
        dict_cursor.execute(q)
        out = dict_cursor.fetchall()
        if not out:
            return 'Empty set'
        return out
    
    elif mode == 'csv':
        if not path:
            path = getcwd()

        path_ = ospath.join(path, 'attendance_export.csv')
        with open(path_, 'w') as outf:
            text_cursor.execute('show columns from attendance')
            header = [i[0] for i in text_cursor.fetchall()]
            writer = csv.DictWriter(outf, fieldnames=header)

            writer.writeheader()
            dict_cursor.execute(q)
            data = dict_cursor.fetchall()

            writer.writerows(data)
            
        return path_