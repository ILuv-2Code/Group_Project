import csv
class Course:
    def __init__(self, c_c:str, c:int): #develop by David Matos
        self.course_code = c_c
        self.credits = c
        self.students = []
    
    def add_student(self, student): #develop by David Matos
        # adds a Student object to the course roster.
        if student not in self.students:
            self.students.append(student)
        else:
            raise ValueError("Student already in course")
    
    def get_student_count(self): #develop by David Matos
        # returns the number of students currently enrolled.
        return len(self.students)

class Student:

    GRADE_POINTS = {
        'A' : 4.0, 'A-' : 3.7,
        'B+': 3.3, 'B' : 3.0, 'B-' : 2.7,
        'C+': 2.3, 'C' : 2.0, 'C-' : 1.7,
        'D' : 1.0,
        'F' : 0.0
        }
    
    def __init__(self, s_i:str, n:str): #develop by David Matos
        if (s_i[0:4] == "STU") and (len(s_i) == 8):
            self.student_id = s_i
        else:
            raise ValueError("Incorrect Student ID")
        
        if n is not None:
            self.name = n
        else: 
            raise ValueError("Empty Name")
        self.courses = {}
    
    def enroll(self, course:Course, grade:str): #develop by David Matos
        if course in self.courses:
            raise ValueError(f"Student is already enrolled in {course.course_code}")
        
        self.courses[course] =  grade
        course.add_student(self)
        
    
    def update_grade(self, course:Course, grade:str): #develop by David Matos
        if course not in self.courses:
            raise ValueError(f"Student not enrolled in course {course.course_code}")
        if grade in self.GRADE_POINTS:
            self.courses[course] = grade
        else:
            raise ValueError("Non-existent grade")
    
    def calculate_gpa(self): #develop by David Matos
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
        return list(self.courses.keys())
    
    def get_course_info(self): #develop by David Matos
        summary = {}
        for course, grade in self.courses.items():
            summary[course] = (course.credits, grade)
        
        return summary
        
    
class University(): #develop by David Matos
    def __init__(self):
        self.students = {} # student id --> student obj
        self.courses = {} # course code --> course obj
        
    def add_course(self, course_code, credits): #develop by David Matos
        # if the course does not exist, create and store it; return the course object.
        if course_code not in self.courses:
            self.courses[course_code] = Course(course_code, credits)
            return self.courses[course_code]
        else:
            return self.courses[course_code]
            
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
            student_id, name, course_data = row
            student = UConn.add_student(student_id, name)
            course_information = course_data.split(';')
            for course_info in course_information:
                if course_info.strip() == "":
                    continue
                course_code, grade = course_info.split(':')
                course = UConn.get_course(course_code)
                if course is not None:
                    student.enroll(course, grade)