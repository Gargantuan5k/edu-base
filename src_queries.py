import mysql.connector
from os import getcwd, path as ospath
import csv
import marks_queries, attendance_queries

try:
    with open('login.txt', 'r') as f:
        s = f.read()
        uname, pwd = tuple(s.split())
except Exception:
    uname = 'root'
    pwd = 'root'

db = mysql.connector.connect(
    host="localhost",
    user=uname,
    password=pwd,
    database="edubase",
    port=3307  # TODO KEEP THIS COMMENTED unless reqd
    )

def close_db():
    db.close()

def get_cursor(dictionary=False):
    # Establish a connection to the MySQL database
    cursor = db.cursor(dictionary=dictionary)
    return cursor

def check_src_exists():
    cursor = get_cursor()
    query = f"select roll_no, name from students_src"
    cursor.execute(query)
    res = cursor.fetchall()

    cursor.close()
    return bool(res)


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
        cursor.execute('delete from marks')
        cursor.execute('delete from attendance')

    students = kwargs['stu_dict']

    for roll_no, name in students.items():
        query = f"insert into students_src(roll_no, name) values('{roll_no}', '{name}')"
        cursor.execute(query)
    
    db.commit()
    cursor.close()
    marks_queries.populate()
    attendance_queries.populate()



def delete_list():
    cursor = get_cursor()
    cursor.execute("delete from students_src")
    cursor.execute('delete from marks')
    cursor.execute('delete from attendance')
    db.commit()
    cursor.close()


def add_student(roll_no, name, exists=False):
    cursor = get_cursor()

    if exists:
        cursor.execute(f"delete from students_src where roll_no = '{roll_no}'")
    
    src_add_query = f"insert into students_src(roll_no, name) values('{roll_no}', '{name}')"
    att_add_query = f"insert into attendance(roll_no, name) values('{roll_no}', '{name}')"
    marks_add_query = f"insert into marks(roll_no, name) values('{roll_no}', '{name}')"
    cursor.execute(src_add_query)
    cursor.execute(att_add_query)
    cursor.execute(marks_add_query)

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
    src_del_query = f"delete from students_src where roll_no = '{roll_no}'"
    att_del_query = f"delete from attendance where roll_no = '{roll_no}'"
    marks_del_query = f"delete from marks where roll_no = '{roll_no}'"    
    cursor.execute(src_del_query)
    cursor.execute(att_del_query)
    cursor.execute(marks_del_query)

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

    src_update_query = f"update students_src set name = '{new_name}' where roll_no = '{roll_no}'"
    marks_update_query = f"update marks set name = '{new_name}' where roll_no = '{roll_no}'"
    att_update_query = f"update attendance set name = '{new_name}' where roll_no = '{roll_no}'"
    cursor.execute(src_update_query)
    cursor.execute(att_update_query)
    cursor.execute(marks_update_query)
    res['new'] = (roll_no, new_name)

    db.commit()
    cursor.close()
    return res

def view(mode, path=None):
    dict_cursor = get_cursor(dictionary=True)
    text_cursor = get_cursor()
    q = 'select * from students_src'

    if mode == 'terminal':
        dict_cursor.execute(q)
        out = dict_cursor.fetchall()
        if not out:
            return 'Empty set'
        return out
    
    elif mode == 'csv':
        if not path:
            path = getcwd()

        path_ = ospath.join(path, 'studentList_export.csv')
        with open(path_, 'w') as outf:
            text_cursor.execute('show columns from students_src')
            header = [i[0] for i in text_cursor.fetchall()]
            writer = csv.DictWriter(outf, fieldnames=header)

            writer.writeheader()
            dict_cursor.execute(q)
            data = dict_cursor.fetchall()

            writer.writerows(data)
            
        return path_
