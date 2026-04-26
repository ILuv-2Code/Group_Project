import unittest 
from project1_2050 import University, Student, Course
class TestCourse(unittest.TestCase): # Test for Course class, using data similar to the CSV file but not directly importing them for easier testing environment.
    def test_object_creation(self): # developed by Mark Le
        course1 = Course("CSE1010", 3)
        self.assertIsInstance(course1, Course)
    def test_add_student(self): # developed by Mark Le
        course1 = Course("CSE1010", 3)
        student1 = Student("STU12345", "Alice Smith")
        course1.add_student(student1)
        self.assertIn(student1, course1.students) # Test to ensure the student is added to the course's student list.
    def test_prevent_duplicate_students(self): # developed by Mark Le
        course1 = Course("CSE1010", 3)
        student1 = Student("STU12345", "Alice Smith")
        course1.add_student(student1)
        self.assertEqual(len(course1.students), 1)  # Ensure only one instance of the student is added
        self.assertRaises(ValueError, course1.add_student, student1)  # Ensure adding the same student again raises an error
    def test_student_count(self): # developed by Mark Le
        course1 = Course("CSE1010", 3)
        student1 = Student("STU12345", "Alice Smith")
        student2 = Student("STU67890", "Bob Johnson")
        course1.add_student(student1)
        course1.add_student(student2)
        self.assertEqual(course1.get_student_count(), 2)
class TestStudent(unittest.TestCase): #test for Student class, using data similar to the CSV file but not directly importing them for easier testing environment.
    def test_object_creation(self): # developed by Mark Le
        student1 = Student("STU12345", "Alice Smith")
        self.assertIsInstance(student1, Student)
    def test_enroll_in_course(self): # developed by Mark Le
        student1 = Student("STU12345", "Alice Smith")
        course1 = Course("CSE1010", 3)
        student1.enroll(course1, "A")
        self.assertIn(course1, student1.courses.keys())
    def test_GPA_calculation(self): # developed by Mark Le
        student1 = Student("STU12345", "Alice Smith")
        course1 = Course("CSE1010", 3)
        course2 = Course("PHYS2010", 2)
        student1.enroll(course1, "A")
        student1.enroll(course2, "B+")
        self.assertAlmostEqual(student1.calculate_gpa(), 3.72 , places=2)
    def test_getting_student_courses(self): # developed by Mark Le
        student1 = Student("STU12345", "Alice Smith")
        course1 = Course("CSE1010", 3)
        course2 = Course("MATH1010", 3)
        student1.enroll(course1, "A")
        student1.enroll(course2, "B")
        self.assertEqual(student1.get_courses(), [course1, course2]) 
class TestUniversity(unittest.TestCase): #test for University class, using data similar to the CSV file but not directly importing them for easier testing environment.
    def test_object_creation(self): # developed by Mark Le
        UConn = University()
        self.assertIsInstance(UConn, University)
    def test_add_course_to_university(self): # developed by Mark Le
        UConn = University()
        course_code1 = "CSE1010"
        credits1 = 3
        UConn.add_course(course_code1, credits1)
        self.assertIn(course_code1, UConn.courses)
    def test_duplicate_course(self): # developed by Mark Le
        UConn = University()
        course_code1 = "CSE1010"
        credits1 = 3
        credits2 = 4
        UConn.add_course(course_code1, credits1)
        UConn.add_course(course_code1, credits2)  # Attempt to add the same course with different credits, the course should not change (should call an extra function update_course in order to do this)
        self.assertEqual(len(UConn.courses), 1)  # Ensure only one instance of the course is added
        self.assertEqual(UConn.courses[course_code1].credits, credits1)  # Ensure the credits of the course remain unchanged
    def test_add_student_to_university(self): # developed by Mark Le
        UConn = University()
        student_id1 = "STU12345"
        name1 = "Alice Smith"
        UConn.add_student(student_id1, name1)
        self.assertIn(student_id1, UConn.students)
    def test_add_duplicate_student(self): # developed by Mark Le
        UConn = University()
        student_id1 = "STU12345"
        name1 = "Alice Smith"
        UConn.add_student(student_id1, name1)
        UConn.add_student(student_id1, name1)  
        self.assertEqual(len(UConn.students), 1)  # Ensure only one instance of the student is added
    def test_get_student_information(self): # developed by Mark Le
        UConn = University()
        student_id1 = "STU12345"
        name1 = "Alice Smith"
        UConn.add_student(student_id1, name1)
        student1 = UConn.get_student(student_id1)
        self.assertEqual(student1.student_id, student_id1)
        self.assertEqual(student1.name, name1)
    def test_get_nonexistent_student(self): # developed by Mark Le
        UConn = University()
        name1 = "Alice Smith"
        student_info = UConn.get_student(name1)
        self.assertIsNone(student_info)
    def test_get_course(self): # developed by Mark Le
        UConn = University()
        course_code1 = "CSE1010"
        credits1 = 3
        UConn.add_course(course_code1, credits1)
        course_info = UConn.get_course(course_code1)
        self.assertEqual(course_info.credits, credits1)
    def test_get_nonexistent_course(self): # developed by Mark Le
        UConn = University()
        course_code1 = "CSE1010"
        course_info = UConn.get_course(course_code1)
        self.assertIsNone(course_info)
if __name__ == '__main__':
    unittest.main()

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