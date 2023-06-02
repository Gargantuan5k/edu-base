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
    if action == 'create':
        students = {}
        while True:
            try:
                num_stu = int(input("Enter the number of students in your classroom: "))

                for i in range(num_stu):
                    students[i+1] = input(f"Enter NAME of student, ROLL NUMBER {i+1}: ")

                create_list(stu_dict=students)
            except:
                print('Invalid data entered! Try again.')
                continue
            break

            
        print('List Successfully Created! You can modify your class list at any time through the same menu.')
        return

    elif action == 'modify':
        while True:
            ch = int(input('Press 1 to delete individual students, 2 to add individual students, 3 to change names, 4 to go back: '))
            if ch == 1: # delete stu
                while True:
                    roll = int(input('Enter roll number to delete, enter 0 to stop.: '))
                    if roll == 0:
                        break

                    res = delete_student(roll_no=roll)
                    if not res:
                        print(f"Roll number {roll} does not exist!")
                    else:
                        print(f"Deleted student {res}")
            
            elif ch == 2: # add stu
                while True:
                    roll = int(input("Enter new roll number, 0 to stop.: "))
                    if roll == 0:
                        break
                    name = input("Enter new name: ")
                    
                    if check_student_rec_exists(roll):
                        yn = input("WARNING: A student with this roll number already exists. Overwrite? (y/N): ").lower().strip()
                        if yn != 'y':
                            continue
                        else:
                            res = add_student(roll_no=roll, name=name, exists=True)
                    else:
                        res = add_student(roll_no=roll, name=name)

                    print(f"Added new student {res}")


            elif ch == 3: # change names
                while True:
                    roll = int(input('Enter roll number to change name, enter 0 to stop.: '))
                    if roll == 0:
                        break
                    new_name = input(f"Enter new name for roll no. {roll}: ")
                    
                    res = update_student(roll_no=roll, new_name=new_name)
                    print(f"Changed student details: {res['original']} -> {res['new']}")

            else:
                return

            return
    
    elif action == 'delete':
        delete_list()
        print('Deleted!')
        return

def run_menu():
    while True:
        print_menu()
        ch = int(input("Enter choice: "))

        # Program:
        if ch == 1:
            print("-----------------")
            print("1. Create a new Students list")
            print("2. Update/modify my current Students List")
            print("3. View my Students List as text or a file")
            print("4. Delete my Students List")
            print("5. Go Back")
            ch1 = int(input("Choose an action: "))

            if ch1 == 1: # Create new list
                exists = check_src_exists()
                if exists:
                    ch2 = input('WARNING: Looks like a student list already exists! Creating/uploading a new list will overwrite the existing one. Proceed?(y/N): ').lower().strip()
                    if ch2 != 'y':
                        continue
                handle_students_list(action='create')
                continue

            elif ch1 == 2: # modify existing list
                exists = check_src_exists()
                if not exists:
                    print("No student list exists! Please create one to get started.")
                    continue
                else:
                    handle_students_list(action='modify')
                    continue

            elif ch1 == 3: # Visualise the existing list TODO
                handle_students_list(action='visualise')

            elif ch1 == 4: # delete entire list
                exists = check_src_exists()
                if not exists:
                    print("No student list exists!")
                    continue
                else:
                    yn = input("WARNING: Delete the students list? This action cannot be undone. (y/N): ").lower().strip()
                    if yn == 'y':
                        handle_students_list(action='delete')
                        continue
                    else:
                        continue

            elif ch1 == 5: # Back
                continue

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
                continue

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
            break

        else:
            print("Please enter valid choice")

if __name__ == '__main__':
    run_menu()
    close_db()