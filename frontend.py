import src_queries
import attendance_queries
import marks_queries
from tkinter import Tk
from tkinter.filedialog import askdirectory as choose_folder
from datetime import date, datetime
from os import system

# Welcome to eduBase!
def print_titlecard():
        with open('ascii/titlecard.txt', 'r') as tcf:
            print(tcf.read())


print_titlecard()

# Thanks!
def print_endcard():
    with open('ascii/endcard.txt', 'r') as ecf:
        print(ecf.read())


def print_help():
    system('cls')
    with open('ascii/what_is_this.txt', 'r') as hf:
        print(hf.read())


# Print menu function
def print_menu():
    print("What would you like to do today?")
    print("(1) Manage my Students List")
    print("(2) Manage my class' Attendance data")
    print("(3) Manage my class' Marks data")
    print("(4) Clear the Screen")
    print("(5) What is this? (HELP FILE)")
    print("(6) Exit")



try:
    # Get today's date
    tdy_date = str(date.today())

    test = ""


    def validate_name(name):
        return name.isalpha()


    def validate_date(date_string):
        try:
            date = datetime.strptime(date_string, '%Y-%m-%d')
            today = datetime.today()

            # Check if the date is not in the future
            if date > today:
                return False

            # Check if the year, month, and day are valid
            year, month, day = date.year, date.month, date.day
            if year < 1 or month < 1 or month > 12 or day < 1:
                return False

            # Check if the day is valid for the given month
            max_day = 31  # Default to maximum days in a month
            if month in {4, 6, 9, 11}:
                max_day = 30
            elif month == 2:
                if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
                    max_day = 29  # Leap year
                else:
                    max_day = 28

            if day > max_day:
                return False

            return True

        except ValueError:
            return False

    def handle_students_list(action='create'):
        if action == 'create': # create a new list
            students = {}
            while True:
                try:
                    num_stu = int(input("Enter the number of students in your classroom: "))

                    for i in range(num_stu):
                        while True:
                            name_stu = input(f"Enter NAME of student, ROLL NUMBER {i+1}: ")
                            valid = validate_name(name_stu)
                            if not valid:
                                print(f"Looks like the name {name_stu} contains non-alphabet characters! Proceed(y) or change(n)? ")
                                proceed_change_yn = input().lower().strip()
                                if proceed_change_yn == 'y':
                                    break
                                else:
                                    continue
                            else:
                                break
                        students[i+1] = name_stu

                    src_queries.create_list(stu_dict=students)
                except:
                    print('Invalid data entered! Try again.')
                    continue
                break

                
            print('List Successfully Created! You can modify your class list at any time through the same menu.')
            return

        elif action == 'modify': # modify existing list
            while True:
                ch = input('Press\n(1) To delete individual students\n(2) To add individual students\n(3) Change names\n(4) Go back\n(5) Clear Screen: ')
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
                            
                            # Validation of name
                            while True:
                                name = input("Enter new name: ")
                                valid = validate_name(name)
                                if not valid:
                                    print(f"Looks like the name {name} contains non-alphabet characters! Proceed(y) or change(n)?")
                                    proceed_change_yn = input().lower().strip()
                                    if proceed_change_yn == 'y':
                                        break
                                    else:
                                        continue
                                else:
                                    break                     
                            
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
                            
                            # Validation of name
                            while True:
                                new_name = input(f"Enter new name for roll no. {roll}: ")
                                valid = validate_name(new_name)
                                if not valid:
                                    print(f"Looks like the name {new_name} contains non-alphabet characters! Proceed(y) or change(n)?")
                                    proceed_change_yn = input().lower().strip()
                                    if proceed_change_yn == 'y':
                                        break
                                    else:
                                        continue 
                                else:
                                    break


                            res = src_queries.update_student(roll_no=roll, new_name=new_name)
                            print(f"Changed student details: {res['original']} -> {res['new']}")
                        except (ValueError, TypeError):
                            print('Invalid data entered!')
                            continue

                elif ch == '4':
                    return
                elif ch == '5':
                    system('cls')
                    continue
                else:
                    print('Invalid data entered!')
                    continue

        
        elif action == 'delete':
            src_queries.delete_list()
            print('Deleted!')
            return
        
        
        elif action == 'visualise':         
            while True:
                print("""View options for STUDENT LIST
    (1) View as Terminal output
    (2) Export list to CSV
    (3) Go Back
    (4) Clear Screen""")
                ch_view = input('Enter option: ')
                if ch_view == '1':
                    out = src_queries.view(mode='terminal')
                    print(out)
                elif ch_view == '2':
                    print('Select Folder to store CSV file')
                    w = Tk()
                    w.withdraw()

                    p = choose_folder(title='Select Folder')
                    out = src_queries.view(mode='csv', path=p)

                    print(out)
                    continue
                elif ch_view == '3':
                    break
                elif ch_view == '4':
                    system('cls')
                    continue
                elif ch_view not in '1234':
                    print('Invalid option!')
                    continue
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

        elif action == 'visualise':         
            while True:
                print("""View options for ATTENDANCE
    (1) View as Terminal output
    (2) Export attendance to CSV
    (3) Go Back
    (4) Clear Screen""")
                
                ch_view = input('Enter option: ')
                if ch_view == '1':
                    out = attendance_queries.view(mode='terminal')
                    print(out)
                elif ch_view == '2':
                    print('Select Folder to store CSV file')
                    w = Tk()
                    w.withdraw()

                    p = choose_folder(title='Select Folder')
                    out = attendance_queries.view(mode='csv', path=p)

                    print(out)
                    continue
                elif ch_view == '3':
                    break
                elif ch_view == '4':
                    system('cls')
                    continue
                elif ch_view not in '1234':
                    print('Invalid option!')
                    continue
            return


    def handle_marks(options):
        res = marks_queries.prepare_table()
        if not res:
            print('Error! You do not have a Students list yet, or your current students list has been mutilated. Please create a new students list to proceed!')
            return
        
        
        if options[0] == 'add':
            mark_l = []
            headers = marks_queries.get_column_headers()
            students = marks_queries.get_students()
            exams = [i for i in headers if i not in ['roll_no', 'name']]

            print('LIST OF EXAMS')
            print('-------------')
            for idx, e in enumerate(exams):
                print(f"({idx+1}) {e}")

            while True:
                ch_exam = int(input('Choose exam: '))
                if ch_exam not in range(1, len(exams) + 1):
                    print('Invalid option!')
                    continue
                break

            exam = exams[ch_exam-1]
            print(f'Entering marks for Exam "{exam}"')


            if options[1] == '1': # all students
                for stu in students:
                    rno = stu.get('roll_no')
                    name = stu.get('name')

                    while True:
                        mark = (input(f'Roll No. {rno} ({name}) [BLANK TO SKIP]: '))
                        if mark:
                            try:
                                mark = int(mark)
                                mark_l.append({'roll_no': rno, f'{exam}': mark})
                                break
                            except:
                                print('Invalid datatype!')
                                continue
                        else:
                            break

                res = marks_queries.add_marks(exam=exam, mark_list=mark_l)
                if not res: print('Error!')
            
            elif options[1] == '2':
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
                    mark = (input(f'Roll No. {rno}, Marks: '))
                    try:
                        mark = int(mark)
                        mark_l.append({'roll_no': rno, f'{exam}': mark})
                        break
                    except:
                        print('Invalid datatype!')
                        continue
                            
                res = marks_queries.add_marks(exam=exam, mark_list=mark_l)
                if not res: print('Error!')                

        elif options[0] == 'delete':
            marks_queries.wipe()
            print('Deleted Successfully!')

        elif options[0] == 'visualise':       
            while True:
                print("""View options for MARKS
    (1) View as Terminal output
    (2) Export mark list to CSV
    (3) Go Back
    (4) Clear Screen""")
                
                ch_view = input('Enter option: ')
                if ch_view == '1':
                    out = marks_queries.view(mode='terminal')
                    print(out)
                elif ch_view == '2':
                    print('Select Folder to store CSV file')
                    w = Tk()
                    w.withdraw()

                    p = choose_folder(title='Select Folder')
                    out = marks_queries.view(mode='csv', path=p)

                    print(out)
                    continue
                elif ch_view == '3':
                    break
                elif ch_view == '4':
                    system('cls')
                elif ch_view not in '1234':
                    print('Invalid option!')
                    continue
            return


    def run_menu(print_options=True):
        while True:
            if print_options: # so that entire menu does not get re-printed every tme user enters invalid input on the main page.
                print_menu()
            else:
                print_options = True
            ch = input("Enter choice: ")
            if ch not in '123456':
                ch = 'err'
            # Program:
            if ch == '1':
                while True:
                    print("-----------------")
                    print("(1) Create a new Students list")
                    print("(2) Update/modify my current Students List")
                    print("(3) View my Students List as text or a file")
                    print("(4) Delete my Students List")
                    print("(5) Go Back")
                    print("(6) Clear Screen")

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

                    elif ch1 == '3': # Visualise the existing list
                        handle_students_list(action='visualise')
                        continue

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
                    
                    elif ch1 == '6':
                        system('cls')
                        continue

                    else:
                        print('Invalid data entered!')
                        continue

            if ch == '2':
                print(f'By default, this will edit the attendance for TODAY {str(date.today())}. If you would like to update attendance for another date, enter it below, or leave it blank to use the default.')
                while True:
                    user_date = input('Enter Date (FORMAT: YYYY-MM-DD): ').strip()
                    if not user_date: break
                    ymd = user_date.split('-')
                    valid = validate_date(user_date)
                    if not valid:
                        print("Invalid date!")
                        continue
                    else:
                        break
                try:
                    ud = datetime(ymd[0], ymd[1], ymd[2])
                    tdy_date = ud
                except:
                    tdy_date = str(date.today())

                print("Enter choice: ")
                
                while True:
                    print("(1) Take Roll Call")
                    print("(2) Mark attendance of specific student(s)")
                    print("(3) Get attendance report")
                    print("(4) Go back")
                    print("(5) Clear Screen")

                    ch1 = input("Enter choice: ")

                    if ch1 == '1':
                        handle_attendance(action='roll', tdy_date=tdy_date)
                        continue
                    
                    elif ch1 == '2':
                        handle_attendance(action='individual', tdy_date=tdy_date)
                        continue
                    
                    elif ch1 == '3':
                        handle_attendance(action='visualise', tdy_date=tdy_date)
                        continue

                    elif ch1 == '4': # back
                        break

                    elif ch1 == '5':
                        system('cls')
                        continue

                    else:
                        print('Invalid data entered!')
                        continue

            elif ch == '3':
                res = marks_queries.prepare_table()
                if not res:
                    print('Error! You do not have a Students list yet, or your current students list has been mutilated. Please create a new students list to proceed!')
                    continue

                while True:
                    print("(1) Modify Mark List")
                    print('(2) View/Export Mark List')
                    print("(3) Go back")
                    print("(4) Clear Screen")
                    ch1 = input("Enter choice: ")
                    if ch1 not in '1234':
                        print('Invalid input!')
                        continue

                    elif ch1 == '4':
                        system('cls')
                        continue

                    elif ch1 == '3':
                        break

                    elif ch1 == '1':
                        while True:
                            print('(1) Add/Modify marks')
                            print('(2) Delete Marks List')
                            print('(3) Go back')
                            print("(4) Clear Screen")
                            ch_add_del = input('Enter Choice: ')
                            if ch_add_del not in '1234':
                                print('Invalid choice!')
                                continue
                            
                            elif ch_add_del == '4':
                                system('cls')
                                continue

                            elif ch_add_del == '3':
                                break

                            elif ch_add_del == '1':
                                while True:
                                    ch_all_single = input('(1) for all students\n(2) for individual student\n(3) Go Back:\n(4) Clear Screen: ').lower().strip()
                                    if ch_all_single not in '1234':
                                        continue
                                    if ch_all_single == '3':
                                        break
                                    if ch_all_single == '4':
                                        system('cls')
                                        continue
                                    handle_marks(['add', ch_all_single])
                                    continue
                            
                                    
                            elif ch_add_del == '2':
                                print("WARNING!! This will PERMANENTLY delete the entire Marks List. This action can't be undone.")
                                proceed_yn = input('Proceed? y/N ')
                                if proceed_yn == 'y':
                                    handle_marks(['delete', None])
                                    continue
                    
                    elif ch1 == '2':
                        handle_marks(['visualise', None])
                        continue

            elif ch == '4':
                system('cls')

            elif ch == '5':
                print_help()
                input()
                system('cls')
                print_titlecard()
                continue

            elif ch == '6':
                print_endcard()
                break

            elif ch == 'err':
                print("Invalid data entered!")
                print_options = False # do not reprint the menu; user has entered invalid data.
                continue

    if __name__ == '__main__':
        run_menu()
        src_queries.close_db()

except KeyboardInterrupt:
    print_endcard()
    exit()