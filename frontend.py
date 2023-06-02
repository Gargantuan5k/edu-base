from queries import *
from datetime import date

# Get today's date
tdy_date = str(date.today())

# Print menu function
def print_menu():
    print("What would you like to do today?")
    print("1. Interact with my Students List")
    print("2. Update Today's Attendance")
    print("3. Update Marks")
    print("4. Update Submissions")
    print("5. Generate report cards")
    print("6. Exit")


def handle_students_list(action='create'):
    students = {}
    while True:
        try:
            num_stu = int(input("Enter the number of students in your classroom: "))

            for i in range(num_stu):
                students[i+1] = input(f"Enter NAME of student, ROLL NUMBER {i+1}: ")

            add_students(stu_dict=students)
        except:
            print('Invalid data entered or DB Error! Try again.')
            continue
        break

        
    print('Students Successfully Added! You can modify your class list at any time through the same menu.')
    run_menu()

def run_menu():
    print_menu()
    ch = int(input("Enter choice: "))

    # Program:
    if ch == 1:
        print("-----------------")
        print("1. Create a new Students list")
        print("2. Update/modify my current Students List")
        print("3. Generate/Visualise my Students List as a file")
        print("4. Go Back")
        ch1 = int(input("Choose an action: "))

        if ch1 == 1: # Create new list
            exists = check_students_exists()
            if exists:
                ch2 = input('WARNING: Looks like a student list already exists! Creating/uploading a new list will overwrite the existing one. Proceed?(y/N): ').lower().strip()
                if ch2 != 'y':
                    run_menu()
            handle_students_list(action='create')

        elif ch1 == 2: # Modify an existing list TODO
            handle_students_list(action='modify')
        elif ch1 == 3: # Visualise the existing list TODO
            handle_students_list(action='visualise')
        elif ch1 == 4: # Back
            run_menu()

    if ch == 2:
        print("Enter choice: ")
        print("1. Mark attendance")
        print("2. Go back")
        ch1 = int(input("Enter choice: "))

        if ch1 == 1:
            add_date(tdy_date=tdy_date)
            rNo = int(input("Enter roll no.: "))
            get_name(rNo)
            confirmation = input("y/n: ")

            if confirmation.lower() == "y":
                markedAttendance = input("Enter attendance(p/a): ")
                mark_att(tdy_date=tdy_date, att=markedAttendance, r_no=rNo)
                print("Attendance Marked!")
            elif confirmation.lower() == "n":
                pass
            else:
                print("Enter valid choice")

        elif ch1 == 2: # back
            run_menu()

    elif ch == 3:
        print("Enter choice: ")
        print("1. Add marks")
        print("2. Add student")
        print("3. Remove student")
        print("4. Go back")

    elif ch == 4:
        print("Enter choice: ")
        print("1. Add Submission")
        print("2. Add student")
        print("3. Remove student")
        print("4. Go back")

    elif ch == 5:
        rNo = int(input("Show report card of which roll no.?: "))

    elif ch == 6:
        exit()

    else:
        print("Please enter valid choice")

if __name__ == '__main__':
    run_menu()