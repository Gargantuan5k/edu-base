import mysql.connector
import src_queries
import csv
from os import getcwd, path as ospath

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
    # port=3307  # TODO KEEP THIS COMMENTED unless reqd
    )

def get_cursor(dictionary=False):
    # Establish a connection to the MySQL database
    cursor = db.cursor(dictionary=dictionary)
    return cursor


def populate():
    cursor = get_cursor()
    cursor.execute('select * from marks')
    r = cursor.fetchall()
    if not r:
        q = f"insert into marks(roll_no, name) select roll_no, name from students_src"
    else:
        q = f"insert into marks(roll_no, name) select roll_no, name from students_src where roll_no not in (select roll_no from marks)"
    cursor.execute(q)
    db.commit()
    cursor.close()


def prepare_table():
    ex = src_queries.check_src_exists()
    if not ex: return False

    cursor = get_cursor()
    populate()

    db.commit()
    cursor.close()
    return True


def get_column_headers():
    cursor = get_cursor(dictionary=True)
    q = 'show columns from marks'
    cursor.execute(q)

    res = cursor.fetchall()
    return [i.get('Field') for i in res]

def get_students():
    cursor = get_cursor(dictionary=True)
    q = 'select roll_no, name from marks'
    cursor.execute(q)

    res = cursor.fetchall()
    return res


def add_marks(exam, mark_list):
    cursor = get_cursor(dictionary=True)
    for i in mark_list:
        roll_no = i.get('roll_no')
        mark = i.get(exam)
        q = f"update marks set `{exam}` = '{mark}' where roll_no = '{roll_no}'"
        cursor.execute(q)
    
    db.commit()
    cursor.close()
    return True


def wipe():
    cursor = get_cursor()
    cursor.execute('delete from marks')
    db.commit()
    cursor.close()


def view(mode, path=None):
    dict_cursor = get_cursor(dictionary=True)
    text_cursor = get_cursor()
    q = 'select * from marks'

    if mode == 'terminal':
        dict_cursor.execute(q)
        out = dict_cursor.fetchall()
        if not out:
            return 'Empty set'
        return out
    
    elif mode == 'csv':
        if not path:
            path = getcwd()

        path_ = ospath.join(path, 'markList_export.csv')
        with open(path_, 'w') as outf:
            text_cursor.execute('show columns from marks')
            header = [i[0] for i in text_cursor.fetchall()]
            writer = csv.DictWriter(outf, fieldnames=header)

            writer.writeheader()
            dict_cursor.execute(q)
            data = dict_cursor.fetchall()

            writer.writerows(data)
            
        return path_
