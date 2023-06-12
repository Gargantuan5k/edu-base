import src_queries
import attendance_queries
import marks_queries
from datetime import date, datetime

# Get today's date
tdy_date = str(date.today())

test = ""

# Print menu function
def print_menu():
    print("What would you like to do today?")
    print("1. Interact with my Students List")
    print("2. Update Today's Attendance")
    print("3. Update Marks")
    print("4. Generate report cards")
    print("5. Exit")


def handle_students_list(action='create'):
    if action == 'create':
        students = {}
        while True:
            try:
                num_stu = int(input("Enter the number of students in your classroom: "))

                for i in range(num_stu):
                    students[i+1] = input(f"Enter NAME of student, ROLL NUMBER {i+1}: ")

                src_queries.create_list(stu_dict=students)
            except:
                print('Invalid data entered! Try again.')
                continue
            break

            
        print('List Successfully Created! You can modify your class list at any time through the same menu.')
        return

    elif action == 'modify':
        while True:
            ch = input('Press 1 to delete individual students, 2 to add individual students, 3 to change names, 4 to go back: ')
            if ch == '1': # delete stu
                while True:
                    try:
                        roll = int(input('Enter roll number to delete, enter 0 to stop.: '))
                        if roll == 0:
                            break

                        res = src_queries.delete_student(roll_no=roll)
                        if not res:
                            print(f"Roll number {roll} does not exist!")
                        else:
                            print(f"Deleted student {res}")
                    except (ValueError, TypeError):
                        print('Invalid data entered!')
                        continue
            
            elif ch == '2': # add stu
                while True:
                    try:
                        roll = int(input("Enter new roll number, 0 to stop.: "))
                        if roll == 0:
                            break
                        name = input("Enter new name: ")
                        
                        if src_queries.check_student_rec_exists(roll):
                            yn = input("WARNING: A student with this roll number already exists. Overwrite? (y/N): ").lower().strip()
                            if yn != 'y':
                                continue
                            else:
                                res = src_queries.add_student(roll_no=roll, name=name, exists=True)
                        else:
                            res = src_queries.add_student(roll_no=roll, name=name)

                        print(f"Added new student {res}")
                    except (ValueError, TypeError):
                        print('Invalid data entered!')
                        continue


            elif ch == '3': # change names
                while True:
                    try:
                        roll = int(input('Enter roll number to change name, enter 0 to stop.: '))
                        if roll == 0:
                            break
                        new_name = input(f"Enter new name for roll no. {roll}: ")
                        
                        res = src_queries.update_student(roll_no=roll, new_name=new_name)
                        print(f"Changed student details: {res['original']} -> {res['new']}")
                    except (ValueError, TypeError):
                        print('Invalid data entered!')
                        continue

            elif ch == '4':
                return
            else:
                print('Invalid data entered!')
                continue

    
    elif action == 'delete':
        src_queries.delete_list()
        print('Deleted!')
        return


def handle_attendance(tdy_date=tdy_date, action='roll'):
    res = attendance_queries.prepare_table(tdy_date)
    if not res:
        print('Error! You do not have a Students list yet, or your current students list has been mutilated. Please create a new students list to proceed!')
        return
    
    if action == 'roll':
        res = attendance_queries.check_unmarked(tdy_date)
        present = []
        absent = []

        if res[0]:
            if not res[1]:
                overwrite_yn = input(f'Looks like some students\' attendances have not been marked for today ({tdy_date}). Would you like to mark these now (Y), or start over, marking all the attendances again (N)? ').lower().strip()
            else:
                overwrite_yn = 'y'
            
            if overwrite_yn == 'y':
                for stu in res[2]:
                    att = input(f'Attendance for Roll {stu[0]} {stu[1]} (p/a), any other key to quit: ').lower().strip()
                    if att == 'p':
                        present.append(stu[0])
                    elif att == 'a':
                        absent.append(stu[0])
                    else:
                        print('Aborting roll call! Your progress has been saved and you can continue marking attendance later.')
                        break
            else:
                for stu in res[3]:
                    att = input(f'Attendance for Roll {stu[0]} {stu[1]} (p/a): ').lower().strip()
                    if att == 'p':
                        present.append(stu[0])
                    else:
                        absent.append(stu[0])

        else:
            overwrite_yn = input(f'Attendance for {tdy_date} has already been recorded! Overwrite? (y/N) ')
            if overwrite_yn == 'y':
                attendance_queries.wipe_attendance(tdy_date)
                handle_attendance()
        
        attendance_queries.mark_attendance(tdy_date=tdy_date, present=present, absent=absent)

    elif action == 'individual':
        present = []
        absent = []

        while True:
            while True:
                try:
                    rno = int(input('Enter roll number (or 0 to quit): '))
                    if rno == 0:
                        return
                    exists = src_queries.check_student_rec_exists(rno)
                    if exists:
                        break
                    print(f"Student with roll number {rno} does not exist!")
                except (ValueError, TypeError):
                    print('Invalid data entered!')
                    continue
        
            while True:
                att = input(f"Enter attendance for Roll {rno} (p/a): ").lower().strip()
                if att == 'p':
                    present.append(rno)
                elif att == 'a':
                    absent.append(rno)
                else:
                    print('Invalid data entered!')
                    continue
                break
            
            attendance_queries.mark_attendance(tdy_date=tdy_date, present=present, absent=absent)

    elif action == 'visualise': pass # TODO

def run_menu(print_options=True):
    while True:
        if print_options: # so that entire menu does not get re-printed every tme user enters invalid input on the main page.
            print_menu()
        else:
            print_options = True
        ch = input("Enter choice: ")
        # Program:
        if ch == '1':
            print("-----------------")
            print("1. Create a new Students list")
            print("2. Update/modify my current Students List")
            print("3. View my Students List as text or a file")
            print("4. Delete my Students List")
            print("5. Go Back")

            while True:
                ch1 = input("Choose an action: ")

                if ch1 == '1': # Create new list
                    exists = src_queries.check_src_exists()
                    if exists:
                        ch2 = input('WARNING: Looks like a student list already exists! Creating/uploading a new list will overwrite the existing one. Proceed?(y/N): ').lower().strip()
                        if ch2 != 'y':
                            continue
                    handle_students_list(action='create')
                    continue

                elif ch1 == '2': # modify existing list
                    exists = src_queries.check_src_exists()
                    if not exists:
                        print("No student list exists! Please create one to get started.")
                        continue
                    else:
                        handle_students_list(action='modify')
                        continue

                elif ch1 == '3': # Visualise the existing list TODO
                    handle_students_list(action='visualise')

                elif ch1 == '4': # delete entire list
                    exists = src_queries.check_src_exists()
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

                elif ch1 == '5': # Back
                    break
                else:
                    print('Invalid data entered!')
                    continue

        if ch == '2':
            print(f'By default, this will edit the attendance for TODAY {str(date.today())}. If you would like to update attendance for another date, enter it below, or leave it blank to use the default.')
            user_date = input('Enter Date (FORMAT: YYYY-MM-DD): ').strip()
            ymd = user_date.split('-')
            try:
                ud = datetime(ymd[0], ymd[1], ymd[2])
                tdy_date = ud
            except:
                tdy_date = str(date.today())

            print("Enter choice: ")
            print("1. Take Roll Call")
            print("2. Mark attendance of specific student(s)")
            print("3. Get attendance report")
            print("4. Go back")
            while True:
                ch1 = input("Enter choice: ")

                if ch1 == '1':
                    handle_attendance(action='roll', tdy_date=tdy_date)
                
                elif ch1 == '2':
                    handle_attendance(action='individual', tdy_date=tdy_date)
                
                elif ch1 == '3':
                    handle_attendance(action='visualise', tdy_date=tdy_date) # TODO

                elif ch1 == '4': # back
                    break
                else:
                    print('Invalid data entered!')
                    continue

        elif ch == '3':
            print("Enter choice: ")
            print("1. Add marks")
            print("4. Go back")
            ch1 = int(input("Enter choice: "))


        elif ch == '4':
            pass # TODO reportcards

        elif ch == '5':
            break

        else:
            print("Invalid data entered!")
            print_options = False # do not reprint the menu; user has entered invalid data.
            continue

if __name__ == '__main__':
    run_menu()
    src_queries.close_db()