import mysql.connector
import src_queries
import frontend
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="edubase",
    # port=3307  # TODO KEEP THIS COMMENTED unless reqd
    )

def get_cursor():
    # Establish a connection to the MySQL database
    cursor = db.cursor()
    return cursor

def populate():
    cursor = get_cursor()
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

def check_unmarked(test): # @returns bool<any unmarked att?>, bool<all att unmarked?>, list[tuple[str<stu_roll>, str<stu_name>]] x2
    cursor = get_cursor()
    q1 = f"select roll_no, name from marks where `{test}` is NULL"
    q2 = f"select roll_no, name from marks"

    cursor.execute(q1)
    unm = cursor.fetchall()
    cursor.execute(q2)
    total = cursor.fetchall()
    cursor.close()

    return bool(unm), (len(unm) == len(total)), unm, total

def addMarks(test):
    cursor = get_cursor()
    adding_query = f"INSERT INTO marks(`{test}`) values('{frontend.st_mark}') where roll_no = '{frontend.rno}'"
    cursor.execute(adding_query)
    db.commit()
    cursor.close()

def wipe_marks(test):
    cursor = get_cursor()
    wipe_q = f"update marks set `{test}` = NULL where roll_no is not NULL"
    cursor.execute(wipe_q)
    db.commit()
    cursor.close()
