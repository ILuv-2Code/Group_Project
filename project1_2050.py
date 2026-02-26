import csv
import random
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
        #Extra Note (by Mark Le): As this function isn't required to return any value, we decided to leave this one as raise ValueError, which is different from the requirements in the University class.
    
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
    
    def __init__(self, s_i:str, n:str): #developed by David Matos, fixed by Mark Le
        if (s_i[0:3] == "STU") and (len(s_i) == 8):
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
    students_in_course = UConn.get_students_in_course(course_code)
    grades = []
    for student in students_in_course:
        course_info = student.get_course_info()
        if course_code in course_info:
            grade = course_info[course_code][1] # grade is the second element in the tuple (credits, grade) in the structure key:value = course: (credits, grades)
            grades.append(grade)
    if grades:
        grade_points = [Student.GRADE_POINTS[grade] for grade in grades]
        mean = sum(grade_points) / len(grade_points)
        mode = max(set(grade_points), key=grade_points.count) #putting the unduplicated grade points in the set, then count based on the initial grade set
        mode_letter = [grade for grade, points in Student.GRADE_POINTS.items() if points == mode][0] #find the letter grade corresponding to the mode grade point
        sorted_grades = sorted(grade_points)
        n = len(sorted_grades)
        median = (sorted_grades[n // 2] if n % 2 != 0 else (sorted_grades[n // 2 - 1] + sorted_grades[n // 2]) / 2)
        print(f"Course Code: {course_code}, Mean GPA: {mean:.2f}, Mode GPA: {mode:.2f}, Mode letter: {mode_letter}, Median GPA: {median:.2f}")
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
    print("Demonstations complete. Thank you for your time!")
                