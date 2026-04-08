import csv
import random
import datetime
class Course:
    def __init__(self, c_c:str, c:int, capacity:int): #develop by David Matos
        self.course_code = c_c
        self.credits = c
        self.capacity = capacity
        self.enrolled_roster = [] #Milestone 2 adaptation, developed by Mark Le, this is the enrolled roster for the course, implemented as a list of EnrollmentRecord objects to store both the student and their enrollment date for each enrolled student in the course.
        self.waitlist = LinkedQueue() #Milestone 2 add-on, developed by Mark Le, this is the waitlist for the course, implemented as a LinkedQueue to follow FIFO order for enrollment from the waitlist when spots open up in the course.
        self.enrolled_sorted_by = None
        self.waitlist_roster = [] #Milestone 2 add-on, developed by Mark Le, this is the waitlist roster for the course, implemented as a list of EnrollmentRecord objects to store both the student and their enrollment date for each student in the waitlist for easy access and duplicate checking when students request enrollment in the course.  
    
    def request_enroll(self, student = None, enroll_date = datetime.date.today()): #develop by David Matos, fixed by Mark Le, milestone 2
        # adds a Student object to the course roster.
        if student is None:
            raise ValueError("Student cannot be None")
        enrollment_record = EnrollmentRecord(student, enroll_date)
        if enrollment_record in self.enrolled_roster:
            print(f"{student.name}, studentID {student.student_id} is already enrolled in this course.")
            return # If duplication happens, we decided not to use raise ValueError as it would disrupt the flow of the program, but we also don't want to just ignore it, so we print a message and continues the loop.
        elif len(self.enrolled_roster) < self.capacity:
            #Extra check to remove from waitlist if the student is already in the waitlist, as we don't want duplication in the waitlist either. This also works for cases where the student is already enrolled, as it would be caught by the first check.
            if enrollment_record in self.waitlist_roster:
                print(f"{student.name}, studentID {student.student_id} is already in the waitlist for this course. Removing from waitlist and enrolling in course.")
                # To remove the student from the waitlist, we need for now to create a temp new waitlist..
                self.remove_waitlist(self, enrollment_record)
            self.enrolled_roster.append(enrollment_record)
        else:
            self.waitlist.enqueue(enrollment_record) # Add to waitlist if course is full
            self.waitlist_roster.append(enrollment_record) # Also add to waitlist roster for easy access and duplicate checking.

    def drop(self, student_id, enroll_date_for_replacement = None): # developed by David Matos
        if self.enrolled_sorted_by != 'id':
            self.sort_enrolled('id', 'bubble')

        index = recursive_binary_search(self.enrolled_roster, student_id, 0, len(self.enrolled_roster)-1)

        if index == -1:
            raise IndexError(f"Student ID {student_id} not found in enrolled roster.")
        
        self.enrolled_roster.pop(index)

        if len(self.waitlist) > 0:
            next_record = self.waitlist.dequeue()
            if enroll_date_for_replacement:
                next_record.enroll_date = enroll_date_for_replacement 
            else:
                next_record.enroll_date = datetime.date.today()
            self.enrolled_roster.append(next_record)
                    
    def get_student_count(self): #develop by David Matos
        # returns the number of students currently enrolled.
        return len(self.enrolled_roster)
    def sort_enrolled(self, by, algorithm): # developed by David Matos
        if algorithm == 'insertion':
            insertion_sort(self.enrolled_roster, by)
        elif algorithm == 'bubble':
            bubble_sort(self.enrolled_roster, by)
        elif algorithm == 'selection':
            selection_sort(self.enrolled_roster, by)
        else:
            raise ValueError("Invalid algorithm. Choose 'insertion', 'selection', or 'bubble'.")
        
        self.enrolled_sorted_by = by

class Student:

    GRADE_POINTS = {
        'A' : 4.0, 'A-' : 3.7,
        'B+': 3.3, 'B' : 3.0, 'B-' : 2.7,
        'C+': 2.3, 'C' : 2.0, 'C-' : 1.7,
        'D' : 1.0,
        'F' : 0.0
        }
    
    def __init__(self, student_id:str, name:str): #developed by David Matos, fixed by Mark Le
        if (student_id[0:3] == "STU") and (len(student_id) == 8):
            self.student_id = student_id
        else:
            raise ValueError("Incorrect Student ID")
        
        if name is not None:
            self.name = name
        else: 
            raise ValueError("Empty Name")
        self.courses = {}
    
    def enroll(self, course:Course, grade:str): #develop by David Matos
        # enrolls student in course and checks whether they're already enrolled
        if course in self.courses:
            raise ValueError(f"Student is already enrolled in {course.course_code}")
        
        self.courses[course] =  grade
        course.request_enroll(student=self)
        
    
    def update_grade(self, course:Course, grade:str): #develop by David Matos
        # updates grade in course IF student is already enrolled
        if course not in self.courses:
            raise ValueError(f"Student not enrolled in course {course.course_code}")
        if grade in self.GRADE_POINTS:
            self.courses[course] = grade
        else:
            raise ValueError("Non-existent grade")
    
    def calculate_gpa(self): #develop by David Matos
        # calculates student GPA using the formula provided
        total_credits = 0
        numerator = 0
        
        for course, grade in self.courses.items():
            numerator += int(course.credits) * self.GRADE_POINTS[grade]
            total_credits += int(course.credits)
            
        if total_credits > 0:
            return (numerator/total_credits)
        else:
            return 0.0
        
    def get_courses(self): #develop by David Matos
        # returns number of keys (number of courses) student has in their course dictionary
        return list(self.courses.keys())
    
    def get_course_info(self): #develop by David Matos
        # returns a simple summary of student performance in the form of course: (credits, grade)
        summary = {}
        for course, grade in self.courses.items():
            summary[course] = (course.credits, grade)
        
        return summary
        
    
class University(): #develop by David Matos
    def __init__(self):
        self.students = {} # student id --> student obj
        self.courses = {} # course code --> course obj
        
    def add_course(self, course_code, credits, capacity): #develop by David Matos
        # if the course does not exist, create and store it; return the course object.
        if course_code not in self.courses:
            self.courses[course_code] = Course(course_code, credits, capacity)
            return self.courses[course_code]
        else:
            return self.courses[course_code]
        
    def update_course(self, course_code, credits): #extra function developed by Mark Le.
        # if the course exists, update the course credits; return the course object.
        if course_code in self.courses: 
            self.courses[course_code].credits = credits
            return self.courses[course_code]
        else:
            raise ValueError("Course doesn't exist")
            
    def add_student(self, student_id, name): #develop by David Matos
        # if the student does not exist, create and store them; return the student object.
        if student_id not in self.students: 
            self.students[student_id] = Student(student_id, name)
            return self.students[student_id]
        else:
            return self.students[student_id]
        

    def get_student(self, student_id): #develop by David Matos
        # returns the student object for that ID (or None if not found).
        return self.students.get(student_id, None)
        
    
    def get_course(self, course_code): #develop by David Matos
        # returns the course object for that code (or None if not found).
        return self.courses.get(course_code, None)
        
    def get_course_enrollment(self, course_code): #develop by David Matos
        # returns the number of students enrolled in the given course.
        if course_code in self.courses:
            return self.courses[course_code].get_student_count()
        else:
            raise ValueError("Course doesn't exist")
    
    def get_students_in_course(self, course_code): #develop by David Matos
        # returns a list of student objects enrolled in the given course
        if course_code in self.courses:
            return self.courses[course_code].students
        else:
            raise ValueError("Course doesn't exist")
        
#Milestone 2 Add-ons:
def insertion_sort(record, by): # developed by David Matos (milestone 2)
    n = len(record)
    for i in range(n):
        j = n-i-1 
        while j < n-1:
            if by == 'name':
                if record[j].student.name.lower() > record[j+1].student.name.lower():
                    record[j], record[j+1] = record[j+1], record[j]
                else:
                    break
            elif by == 'id':
                if record[j].student.student_id > record[j+1].student.student_id:
                    record[j], record[j+1] = record[j+1], record[j]
                else:
                    break
            elif by == 'date':
                if record[j].enroll_date > record[j+1].enroll_date:
                    record[j], record[j+1] = record[j+1], record[j]
                else:
                    break
            else:
                raise ValueError("Choose 'name', 'id', or 'date'")
            j += 1

def selection_sort(record, by): # developed by David Matos
    for i in range(len(record)-1):
        max_j = 0
        for j in range(len(record)-i):
            if by == 'name':
                if record[j].student.name.lower() > record[max_j].student.name.lower():
                    max_j = j
            elif by == 'id':
                if record[j].student.student_id > record[max_j].student.student_id:
                    max_j = j
            elif by == 'date':
                if record[j].enroll_date > record[max_j].enroll_date:
                    max_j = j
            else:
                raise ValueError("Choose 'name', 'id', or 'date'")

        if (len(record)-i-1) != max_j:
            record[len(record)-i-1], record[max_j] = record[max_j], record[len(record)-i-1]

def bubble_sort(record, by): # developed by David Matos (milestone 2)
    n = len(record)
    for i in range(n-1):
        swapped = False
        for j in range(n-1-i):
            if by == 'name':
                if record[j].student.name.lower() > record[j+1].student.name.lower():
                    record[j], record[j+1] = record[j+1], record[j]
                    swapped = True
            elif by == 'id':
                if record[j].student.student_id > record[j+1].student.student_id:
                    record[j], record[j+1] = record[j+1], record[j]
                    swapped = True
            elif by == 'date':
                if record[j].enroll_date > record[j+1].enroll_date:
                    record[j], record[j+1] = record[j+1], record[j]
                    swapped = True
            else:
                raise ValueError("Choose 'name', 'id', or 'date'")
        if not swapped:
            break

def recursive_binary_search(records, target_id, low, high): # developed by David Matos (milestone 2)
    if low > high:
        return -1
    mid = (low + high) // 2
    current_id = records[mid].student.student_id
    if current_id == target_id:
        return mid
    elif target_id < current_id:
        return recursive_binary_search(records, target_id, low, mid - 1)
    else:
        return recursive_binary_search(records, target_id, mid + 1, high)

class EnrollmentRecord: #developed by Mark Le, milestone 2
    def __init__(self, student = None, enroll_date = datetime.date.today()):
        if student is None:
            raise ValueError("Student cannot be None")
        self.student = student
        self.enroll_date = enroll_date
        
# Task 2 - LinkedQueue ADT, developed by Mark Le, milestone 2:
class Node:
    def __init__(self, data = None):
        self.data = data
        self.next = None

class LinkedQueue: #Single linked list adaptation for LinkedQueue
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    def __len__(self):
        return self.size
    def is_empty(self):
        return len(self) == 0
    def enqueue(self, data): #Follows FIFO, this resembles add_last
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    def dequeue(self): #Follows FIFO, this resembles remove_first 
        if self.is_empty():
            raise ValueError("Waitlist is empty! Cannot dequeue from an empty waitlist.")
        data = self.head.data
        self.head = self.head.next
        self.size -= 1
        if self.is_empty():
            self.tail = None
        return data

'''
if __name__ == "__main__":
    # Demonstrations, developed by Mark Le
    print("Demonstation: University Course and Student Management System")
    print("-------------------------------------------------------------")
    UConn = University() #Initializes University object
    with open('course_catalog.csv', 'r') as f: # Reads course catalog and adds courses to UConn
        course_reader = csv.reader(f, delimiter=',')
        next(course_reader) # skip header row
        for row in course_reader:
            course_code, credits = row
            UConn.add_course(course_code, credits)
    with open('university_data.csv', 'r') as f: # Reads student enrollments and adds students (name + id) and their course enrollments to UConn
        student_reader = csv.reader(f, delimiter=',')
        next(student_reader) # skip header row
        for row in student_reader:
            student_id, name, course_data, gpa = row # I believe adding gpa to the CSV file is a readability mistake, as it forces an "empty" column that I don't think is at all necessary, but I left it in for the sake of consistency with the provided CSV file. The gpa column is not used in the code, as the GPA is calculated based on the course enrollments and grades for each student.
            student = UConn.add_student(student_id, name)
            course_class_and_grades = course_data.split(';')
            for course_info in course_class_and_grades:
                if course_info.strip() == "":
                    continue
                course_code, grade = course_info.split(':')
                course = UConn.get_course(course_code)
                if course is not None:
                    student.enroll(course, grade)
                else:
                    raise ValueError(f"{course_code} not found in university catalog. Please check your course information again.")
    print("University data loaded complete.")
    print("-------------------------------------------------------------")
    print("Starting demonstrations...")
    print("-------------------------------------------------------------")
    print("Demo 1: Get list of students enrolled in a course")
    print("Choosing a random course within the catalog") # Example course code 
    course_codes = list(UConn.courses.keys())
    course_code = random.choice(course_codes) #course_code can be designated for specific instances, but is currently set to random for demonstration purposes.
    students_in_course = UConn.get_students_in_course(course_code)
    print(f"Students enrolled in {course_code}:")
    count_num = 1
    for student in students_in_course:
        print(f"{count_num}) ID: {student.student_id}, Name: {student.name}")
        count_num += 1
    print("-------------------------------------------------------------")
    print("Demo 2: Print GPA of a student")
    print("Choosing a random student from the university data...")
    student_ids = list(UConn.students.keys())
    student_id = random.choice(student_ids) #student_id can be designated for specific instances, but is currently set to random for demonstration purposes.
    student = UConn.get_student(student_id) 
    if student is not None:
        gpa = student.calculate_gpa()
        print(f"GPA of student {student.name} (ID: {student.student_id}): {gpa:.2f}")
    else:
        print(f"Student with ID {student_id} not found.") #This is for double check, and works for changing for specific IDs for actual instances.
    print("-------------------------------------------------------------")  
    print("Demo 3: Print all the courses and course info ( grades and credits ) for a student")
    print("Choosing a random student from the university data...")
    student_id = random.choice(student_ids) #student_id can be designated for specific instances, but is currently set to random for demonstration purposes.
    student = UConn.get_student(student_id)
    if student is not None:
        course_info = student.get_course_info()
        print(f"Course information for student {student.name} (ID: {student.student_id}):")
        for course, (credits, grade) in course_info.items():
            print(f"Course Code: {course.course_code}, Credits: {credits}, Grade: {grade}")
    else:
        print(f"Student with ID {student_id} not found.") #This is for double check, and works for changing for specific IDs for actual instances.
    print("-------------------------------------------------------------")
    print("Calculate mean, mode and median for a course")
    print("Choosing a random course within the catalog...")
    course_code = random.choice(course_codes) #course_code can be designated for specific instances, but is currently set to random for demonstration purposes.
    course = UConn.get_course(course_code) # Getting the course object as Student.get_course_info() returns a dictionary with course objects as keys.
    students_in_course = UConn.get_students_in_course(course_code)
    grades = []
    for student in students_in_course:
        course_info = student.get_course_info()
        if course in course_info:
            grade = course_info[course][1] # grade is the second element in the tuple (credits, grade) in the structure key:value = course: (credits, grades)
            grades.append(grade)
    if grades:
        grade_points = [Student.GRADE_POINTS[grade] for grade in grades]
        mean = sum(grade_points) / len(grade_points)
        mode = max(set(grade_points), key=grade_points.count) #putting the unduplicated grade points in the set, then count based on the initial grade set
        mode_letter = [grade for grade, points in Student.GRADE_POINTS.items() if points == mode][0] #find the letter grade corresponding to the mode grade point
        sorted_grades = sorted(grade_points)
        n = len(sorted_grades)
        median = (sorted_grades[n // 2] if n % 2 != 0 else (sorted_grades[n // 2 - 1] + sorted_grades[n // 2]) / 2)
        median_letter = [grade for grade, points in Student.GRADE_POINTS.items() if points == median][0]
        print(f"Course Code: {course_code}, Mean GPA: {mean:.2f}, Mode GPA: {mode:.2f}, Mode letter: {mode_letter}, Median GPA: {median:.2f}, Median letter: {median_letter}")
    else:
        print(f"No grades found for course {course_code}.")
    print("-------------------------------------------------------------")
    print("Demo 5: Calculate mean and median for the GPA of all students in the university")
    gpas = []
    for student in UConn.students.values(): #Grabbing student values, in this dictionary, the whole Student object is stored in the value.
        gpa = student.calculate_gpa()
        gpas.append(gpa)
    if gpas: #Checking validity of gpas list to avoid division by zero error, and works for cases where there are no students in the university data.
        mean_gpa = sum(gpas) / len(gpas)
        sorted_gpas = sorted(gpas)
        n = len(sorted_gpas)
        median_gpa = (sorted_gpas[n // 2] if n % 2 != 0 else (sorted_gpas[n // 2 - 1] + sorted_gpas[n // 2]) / 2)
        print(f"Mean GPA of all students: {mean_gpa:.2f}, Median GPA of all students: {median_gpa:.2f}")
    else:
        print("No students found in the university.")
    print("-------------------------------------------------------------")
    print("Demo 6: Print common students in two different courses:")
    course_code1, course_code2 = random.sample(course_codes, 2) #Randomly select 2 different courses for demonstration purposes, can be designated for specific instances.
    students_in_course1 = set(UConn.get_students_in_course(course_code1)) #Using set to avoid duplication while also reducing time complexity for finding common students between the two courses from O(n^2) to O(n)
    students_in_course2 = set(UConn.get_students_in_course(course_code2))
    common_students = students_in_course1.intersection(students_in_course2)
    print(f"Course 1: {course_code1}, Course 2: {course_code2}")
    if common_students:
        print("Common students enrolled in both courses:")
        count_num = 1
        for student in common_students:
            print(f"{count_num}) ID: {student.student_id}, Name: {student.name}")
            count_num += 1
    else:
        print("No common students enrolled in both courses.")
    print("-------------------------------------------------------------")
    print("Demonstrations complete. Thank you for your time!")
'''              