import mysql.connector
from os import getcwd, path as ospath
import csv

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
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

    students = kwargs['stu_dict']

    for roll_no, name in students.items():
        query = f"insert into students_src(roll_no, name) values('{roll_no}', '{name}')"
        cursor.execute(query)
    
    db.commit()
    cursor.close()


def delete_list():
    cursor = get_cursor()
    cursor.execute("delete from students_src")
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
