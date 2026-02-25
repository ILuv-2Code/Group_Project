class Course:
    def __init__(self, c_c:str, c:int, s:list): #develop by David Matos
        self.course_code = c_c
        self.credits = c
        self.students = s
    
    def add_student(self, student): #develop by David Matos
        # adds a Student object to the course roster.
        self.students.append(student)
        pass 
    
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
    
    def __init__(self, s_i:str, n:str, c:dict): #develop by David Matos
        self.student_id = s_i
        self.name = n
        self.courses = c
    
    def enroll(self, course, grade): #develop by David Matos
        self.courses[course] =  grade
        course.add_student(self)
        
    
    def update_grade(self, course, grade): #develop by David Matos
        self.courses[course] = grade
    
    def calculate_gpa(self): #develop by David Matos
        # refer to grade clac. on pdf
        pass
    
    def get_courses(self): #develop by David Matos
        return self.courses.keys()
    
    def get_course_info(self): #develop by David Matos
        #returns a structured summary of all enrollments, including course code, grade, and credits
        pass
    
class University(): #develop by David Matos
    def __init__(self, s:dict, c:dict):
        self.students = s
        self.courses = c
        
    def add_course(self, course_code, credits): #develop by David Matos
        # if the course does not exist, create and store it; return the course object.
        pass

    def add_student(self, student_id, name): #develop by David Matos
        # if the student does not exist, create and store them; return the student object.
        pass

    def get_student(self, student_id): #develop by David Matos
        # returns the student object for that ID (or None if not found).
        pass
    
    def get_course(self, course_code): #develop by David Matos
        # returns the course object for that code (or None if not found).
        pass
        
    def get_course_enrollment(self, course_code): #develop by David Matos
        # returns the number of students enrolled in the given course.
        pass
    
    def get_students_in_course(self, course_code): #develop by David Matos
        # returns a list of student objects enrolled in the given course
        pass