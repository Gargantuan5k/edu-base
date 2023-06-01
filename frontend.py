from main import *
from datetime import date

# Get today's date
tdy_date = str(date.today())

# Print menu function
def print_menu():
    print("What would you like to do today?")
    print("1. Update Attendance")
    print("2. Update Marks")
    print("3. Update Submissions")
    print("4. Get report card")
    print("5. Exit")

print_menu()

# Get user choice
ch = int(input("Enter choice(1/2/3/4/5): "))

# Program:
if ch == 1:
    print("Enter choice: ")
    print("1. Mark attendance")
    print("2. Add student")
    print("3. Remove student")
    print("4. Go back")
    ch1 = int(input("Enter choice: "))

    if ch1 == 1:
        mysql_query_1()
        rNo = int(input("Enter roll no.: "))
        mysql_query_2()
        confirmation = input("y/n: ")
        if confirmation.lower() == "y":
            markedAttendance = input("Enter attendance(p/a): ")
            mysql_query_3()
            print("Attendance Marked!")
        elif confirmation.lower() == "n":
            pass
        else:
            print("Enter valid choice")
    elif ch1 == 2:
        table = "attendance"
        rNo = int(input("Enter new student's roll no.: "))
        Name = input("Enter new student's name: ")
        mysql_query_4()
    elif ch1 == 3:
        table = "attendance"
        rNo = int(input("Enter roll no. of student to remove: "))
        mysql_query_5()
        confirmation = input("y/n: ")
        if confirmation.lower() == "y":
            mysql_query_6()
            print("Student removed!")
        else:
            pass
    elif ch1 == 4:
        print_menu()
elif ch == 2:
    print("Enter choice: ")
    print("1. Add marks")
    print("2. Add student")
    print("3. Remove student")
    print("4. Go back")

elif ch == 3:
    print("Enter choice: ")
    print("1. Add Submission")
    print("2. Add student")
    print("3. Remove student")
    print("4. Go back")

elif ch == 4:
    rNo = int(input("Show report card of which roll no.?: "))

elif ch == 5:
    exit()

else:
    print("Please enter valid choice")

