import mysql.connector
from main import tdy_date

# Establish a connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="edubase"
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Write your SQL query to add a new column to the table
alter_query = f"ALTER TABLE attendance ADD COLUMN `{tdy_date}` varchar(20)"

# Execute the SQL query
cursor.execute(alter_query)

# Commit the changes to the database
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()