GRADE_TABLE = {'A+': 4, 'A': 4, 'A-': 3.7,
               'B+': 3.3, 'B': 3, 'B-': 2.7,
               'C+': 2.3, 'C': 2, 'C-': 1.7,
               'D+': 1.3, 'D': 1, 'D-': 0.7,
               'F': 0}


class Course(object):
    def __init__(self, department, number, name, course_credits):
        self.department = department
        self.number = number
        self.name = name
        self.credits = int(course_credits)

    def __repr__(self):
        return f'Course {self.department} {self.number}: {self.name}, credit {self.credits}'


class CourseOffering(object):
    QUARTER_TABLE = {'WINTER': 1, 'SPRING': 2, 'SUMMER': 3, 'FALL': 4}

    def __init__(self, at_institution, course, section_number, instructor, year, quarter):
        try:
            self.school = at_institution
            self.course = course
            self.section_number = section_number
            self.instructor = instructor
            self.year = year
            self.quarter = quarter
            if quarter not in QUARTER_TABLE:
                raise KeyError
            else:
                self.quarter_num = CourseOffering.QUARTER_TABLE[quarter]
            self.registered_students = {}
            self.grades = {}
        except KeyError:
            print('Please input correct quarter (case sensitive)!')

    def __repr__(self):
        return f'{self.course}, offered on {self.quarter} {self.year}'

    def register_students(self, *students_username_args):
        try:
            for student_username in students_username_args:
                if student_username not in self.school.enrolled_student:
                    print(f'Student {student_username} not enrolled!')
                else:
                    if student_username in self.registered_students:
                        raise ValueError
                    else:
                        # Add student object from school to registered students, saving username as key
                        self.registered_students[student_username] = self.school.enrolled_student[student_username]
                        print(f'{student_username} successfully registered to course!')
        except ValueError:
            print(f'\n{student.username} is already registered for the course!\n')

    def get_students(self):
        return self.registered_students

    def submit_grade(self, student_username, letter_grade):
        #  Takes an instance of the student class
        #  and a letter grade (e.g., A+, A, A-, B+, B, B-, ...)
        #  and sets the student's letter grade for the course.
        #  If the grade has already been set, this operation overwrites the existing grade.
        try:
            if student_username not in self.registered_students:
                raise ValueError
            else:
                if student_username in self.grades.keys():
                    print(f'{student_username} already has a grade and is overwritten.')
                if letter_grade not in GRADE_TABLE:
                    raise KeyError
                else:
                    self.grades[student_username] = letter_grade
                    print(f'{student_username}\'s grade for this course is {self.grades[student_username]}')
        except ValueError:
            print(f'\n{student_username} is not in record!\n')
        except KeyError:
            print(f'\nPlease enter correct letter grade! (UPPER LETTER WITH SYMBOL)\n')

    def get_grade(self, student_username):
        if self.grades[student_username] is None:
            return 0
        return self.grades[student_username]


class Institution(object):
    def __init__(self, name):
        self.name = name
        self.enrolled_student = {}
        self.instructors = {}
        self.domain = f"{self.name.lower().replace(' ','_')}.edu"
        self.course_catalog = {}
        self.course_offerings = {}

    def __repr__(self):
        return f'{self.name}'

    def list_student(self):
        return self.enrolled_student

    def enroll_student(self, last_name, first_name, username):
        last_name = last_name
        first_name = first_name
        username = username
        if username in self.enrolled_student:
            print(f'{first_name} {last_name} already enrolled!')
        else:
            self.enrolled_student[username] = Student(last_name, first_name, username)
            self.enrolled_student[username].enrolled(self)
            print(f'{self.enrolled_student[username].first_name} {self.enrolled_student[username].last_name} '
                  f'successfully enrolled!')

    def list_instructors(self):
        return self.instructors

    def hire_instructor(self, last_name, first_name, username):
        last_name = last_name
        first_name = first_name
        username = username
        if username in self.instructors:
            print(f'Instructor {first_name} {last_name} already hired!')
        else:
            self.instructors[username] = Instructor(last_name, first_name, username)
            self.instructors[username].hired(self)
            print(f'{self.instructors[username].first_name} {self.instructors[username].last_name} '
                  f'successfully hired!')

    def assign_instructor(self, instructor_username, department, number, year, quarter):
        try:
            if instructor_username not in self.instructors:
                raise KeyError('Instructor', instructor_username)
            else:
                instructor = self.instructors[instructor_username]
            if (department, number, quarter, year) not in self.course_offerings:
                raise KeyError('Course', department+number)
            else:
                course_offering = self.course_offerings[(department,number, quarter, year)]
            course_offering.instructor = instructor
            print(f'{course_offering} now has instructor {course_offering.instructor}')
        except KeyError as ke:
            print(f'\n{ke.args[0]} does not have {ke.args[1]}!\n')

    def list_course_catalog(self):
        # All courses available
        return self.course_catalog

    def list_course_schedule(self, year, quarter, department=None):
        schedule = {}
        if not department:
            for key, offered_course in self.course_offerings.items():
                if key[3] == year and key[2] == quarter:
                    print('added')
                    schedule[key] = offered_course
        else:
            for key, offered_course in self.course_offerings.items():
                if key[3] == year and key[2] == quarter and department == key[0]:
                    print('added')
                    schedule[key] = offered_course
        return schedule

    def add_course(self, department, number, name, course_credits):
        department = department
        number = number
        name = name
        course_credits = course_credits
        if department+number in self.course_catalog:
            print('Course already exists! Overwriting...')
            # Add to catalog
        self.course_catalog[(department, number)] = Course(department, number, name, course_credits)

    def add_course_offering(self, department, number, section_number, instructor_username, year, quarter):
        try:
            if (department, number) not in self.course_catalog:
                raise KeyError('Course catalog', department+number)
            else:
                course = self.course_catalog[(department, number)]
            if instructor_username not in self.instructors:
                raise KeyError('Instructor', instructor_username)
            else:
                instructor = self.instructors[instructor_username]  # instructor Object
            section_number = section_number
            year = year
            quarter = quarter
            # Add to schedule
            if (department, number, quarter, year) in self.course_offerings:
                print('Overwriting existing course offering...')
            self.course_offerings[(department, number, quarter, year)] = CourseOffering(
                self, course, section_number, instructor, year, quarter)
            print('Course Offering Added!')
            print(f'{self.course_offerings[(department, number, quarter, year)]} '
                  f'is taught by {self.course_offerings[(department, number, quarter, year)].instructor}')
        except KeyError as ke:
            print(f'\n{ke.args[1]} is not recorded in {ke.args[0]}! Please add it first\n')


class Person(object):
    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name
        self.school = None
        self.username = None
        self.affiliation = None
        self.email = None


class Instructor(Person):
    def __init__(self, last_name, first_name, username):
        Person.__init__(self, last_name, first_name)
        self.username = username
        self.affiliation = 'Instructor'
        self.school = None

    def __repr__(self):
        return f'Instructor {self.first_name} {self.last_name}, username: {self.username}'

    def list_courses(self, year=None, quarter=None):
        course_lst = []
        for oc_key, oc_obj in self.school.course_offerings.items():
            if oc_obj.instructor == self:
                if oc_key[2] == year if year else True and oc_key[1] == quarter if quarter else True:
                    course_lst.append(oc_obj)
        sorted_course_lst = sorted(course_lst, key=lambda x: (int(x.year), x.quarter_num), reverse=True)
        return sorted_course_lst

    def hired(self, school):
        self.school = school
        self.email = f'{self.username}@{self.school.domain}'


class Student(Person):
    def __init__(self, last_name, first_name, username):
        Person.__init__(self, last_name, first_name)
        self.username = username
        self.affiliation = 'Student'
        self.school = None

    def __repr__(self):
        return f'Student {self.first_name} {self.last_name}, username: {self.username}'

    def enrolled(self, school):
        self.school = school
        self.email = f'{self.username}@{self.school.domain}'

    def list_courses(self):
        # Courses has taken
        course_lst = []
        for offered_course in self.school.course_offerings.values():  # All offered courses
            # Go through registered students (objects) for the course
            if self in offered_course.registered_students.values():
                course_lst.append(offered_course)
        sorted_course_lst = sorted(course_lst, key=lambda x: (int(x.year), x.quarter_num), reverse=True)
        return sorted_course_lst

    def earned_credits(self):
        # Number of credits earned
        credit = 0
        for taken_course in self.list_courses():
            credit += taken_course.course.credits
        return credit

    def gpa(self):
        # Return gpa
        try:
            gp = 0
            credit_count = 0
            for taken_course in self.list_courses():
                gp += taken_course.course.credits * GRADE_TABLE[taken_course.get_grade(self.username)]
                credit_count += taken_course.course.credits
            gpa = gp/credit_count
            return gpa
        except KeyError:
            print(f'\nno grade records on {taken_course}\n')

        except ZeroDivisionError:
            print(f'\nNo course records for student!\n')

