import mysql.connector
from main import tdy_date, markedAttendance, Name

# Establish a connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="edubase"
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Check if the date column already exists in the table
check_query = f"SHOW COLUMNS FROM attendance LIKE '{tdy_date}'"
cursor.execute(check_query)
result = cursor.fetchone()

# Add the date as column to the table if it doesn't already exist
if result is None:
    alter_query = f"ALTER TABLE attendance ADD COLUMN `{tdy_date}` varchar(20)"
    
    # Execute the SQL query
    cursor.execute(alter_query)

#add attendance of specific student
attendance_query = f"UPDATE attendance SET `{tdy_date}` = `{markedAttendance}` WHERE name = `{Name}`"

# Execute the SQL query
cursor.execute(attendance_query)

# Commit the changes to the database
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()