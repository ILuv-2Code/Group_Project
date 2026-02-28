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