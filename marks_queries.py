import mysql.connector
import src_queries

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


