#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import pandas as pd
import pickle as pk
from pathlib import Path
import registrar

data = Path('./data')
if not data.exists():
    data.mkdir()
del data

school = input('Welcome to the Registration System\nPlease enter the name of your institution: ')
while not school:
    print('Please assign a name!')
    school = input('Please enter the name of your institution: ')
path = Path(f'./data/{school}.pkl')
active_school = registrar.Institution(school)
if path.exists():
    with open(path, 'rb') as source:
        active_school = pk.load(source)
    print('The school already exists and is retrieved.')
#The usage of pickle is learned from Miss Yunhua Xu

print(f'Currently working on school {active_school}, the domain name will be \'{active_school.domain}\'')


# Input loop style inspired by Mr Ruizhe Zhou
while True:
    try:
        print('Please select an option from the following:',
              '1 Create a course',
              '2 Schedule a course offering ',
              '3 List course catalog',
              '4 List course schedule ',
              '5 Hire an instructor',
              '6 Assign a new instructor to a course ',
              '7 Enroll a student ',
              '8 Register a student for a course ',
              '9 List enrolled students ',
              '10 List students registered for a course',
              '11 Submit student grade',
              '12 Get student records',
              '13 Exit', sep='\n')
        choice = input('Please enter your choice (only entering 13 could Exit):')
        if choice == '1':
            print('Creating a new course')
            print('Style Example: MATH, 101, Intro to math, 3')
            input_prompt = ['department', 'number', 'name', 'course_credits']
            user_input = []
            for i in input_prompt:
                user_input.append(input(f'Please input {i}: '))
            active_school.add_course(*user_input)
            print('Course Added!')

        elif choice == '2':
            print('Scheduling a course offering')
            print('Style Example: MATH, 101, 2, jseed, 2017, FALL')
            input_prompt = ['department', 'course number', 'section', 'instructor', 'year', 'quarter (WINTER, SPRING, SUMMER, or FALL)']
            user_input = []
            for i in input_prompt:
                user_input.append(input(f'Please input {i}: '))
            active_school.add_course_offering(*user_input)

        elif choice == '3':
            course_catalog = pd.Series(active_school.list_course_catalog())
            print('Listing Course catalogs:')
            print(course_catalog)

        elif choice == '4':
            print('Please input year, quarter, and department(if necessary)')
            year = input('Please input year (in full digits): ')
            quarter = input('Please input quarter (FALL, WINTER, SPRING, or SUMMER): ')
            department = input('Please input department: ')
            schedule = pd.Series(active_school.list_course_schedule(year, quarter, department))
            print(schedule)

        elif choice == '5':
            print('Hiring new instructor!')
            print('Style Example: Appleseed, John, jseed')
            input_prompt = ['last name','first name', 'username']
            user_input = []
            for i in input_prompt:
                user_input.append(input(f'Please input {i}: '))
            active_school.hire_instructor(*user_input)

        elif choice == '6':
            confirm = input('This will replace current instructor for desired course. continue? y/n: ')
            if confirm == 'n':
                raise KeyboardInterrupt
            else:
                print('Style Example: jseed, MATH, 101, 2017, FALL')
                input_prompt = ['instructor username', 'department', 'course number','year','quarter']
                user_input = []
                for i in input_prompt:
                    user_input.append(input(f'Please input {i}: '))
                active_school.assign_instructor(*user_input)

        elif choice == '7':
            print('Enrolling a new student!')
            print('Style Example: Appleseed, Johnson, jseeds')
            input_prompt = ['last name', 'first name', 'username']
            user_input = []
            for i in input_prompt:
                user_input.append(input(f'Please input {i}: '))
            active_school.enroll_student(*user_input)

        elif choice == '8':
            try:
                print('Register student(s) to a course!')
                department = input('Please input course department: ')
                number = input('Please input course number: ')
                year = input('Please define year: ')
                quarter = input('Please provide which quarter: ')
                if (department, number, quarter, year) not in active_school.course_offerings:
                    raise KeyError
                else:
                    course = active_school.course_offerings[(department, number, quarter, year)]
                    user_input = []
                    while True:
                        if input('Continue? y/n: ') == 'n':
                            break
                        user_input.append(input('Please input student username: '))
                    course.register_students(*user_input)
            except KeyError:
                print(f'\n{department+number} is not offered on {quarter+year}\n')


        elif choice == '9':
            print('Listing students enrolled.')
            students = pd.Series(active_school.list_student())
            print(students)

        elif choice == '10':
            try:
                print('Listing registered students for a course')
                department = input('Please input course department: ')
                number = input('Please input course number: ')
                year = input('Please define year: ')
                quarter = input('Please provide which quarter: ')
                if (department, number, quarter, year) not in active_school.course_offerings:
                    raise KeyError
                else:
                    course = active_school.course_offerings[(department, number, quarter, year)]
                    students = pd.Series(course.get_students())
                    print(students)

            except KeyError:
                print(f'\n{department+number} is not offered on {quarter+year}\n')

        elif choice == '11':
            try:
                print('Submitting grade for a student in course.')
                department = input('Please input course department: ')
                number = input('Please input course number: ')
                year = input('Please define year: ')
                quarter = input('Please provide which quarter: ')
                if (department, number, quarter, year) not in active_school.course_offerings:
                    raise KeyError
                else:
                    course = active_school.course_offerings[(department, number, quarter, year)]
                    student = input('Please assign student username to search for the student: ')
                    print('Letter grades available: (A, B, C, D,)(+,,-) and F')
                    grade = input(f'Please give student {student} a letter grade: ')
                    course.submit_grade(student, grade)
            except KeyError:
                print(f'\n{department+number} is not offered on {quarter+year}\n')

        elif choice == '12':
            try:
                print('Showing student\'s records.')
                student = input('Please assign student\'s username to search: ')
                if student not in active_school.enrolled_student:
                    raise KeyError
                student_in_record = active_school.enrolled_student[student]
                courses_taken = pd.Series(student_in_record.list_courses(),
                                          index=[f'{course.quarter+course.year}' for course in student_in_record.list_courses()])
                earned_credits = student_in_record.earned_credits()
                gpa = student_in_record.gpa()
                print(f'Student name: {student_in_record.first_name} {student_in_record.last_name}',
                      f'Student username: {student_in_record.username}',
                      f'email: {student_in_record.email}',
                      'Course taken:',
                      courses_taken,
                      'Credits earned:',
                      earned_credits,
                      'GPA:',
                      gpa,
                      sep='\n')
            except KeyError:
                print(f'\nStudent {student} not in record!\n')

        elif choice == '13':
            break
    except KeyboardInterrupt:
        continue

with open(f'./data/{active_school.name}.pkl', 'wb') as output:
    pk.dump(active_school,output,pk.HIGHEST_PROTOCOL)
del active_school
print('Program exited.')
