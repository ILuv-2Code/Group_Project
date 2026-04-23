#Create tests for everything done in milestone 3, including the new HashMap implementation and the changes to the Course class. We will use the unittest framework for this.
#Developed by Mark Le
import unittest
from project1_2050 import *
import datetime
class TestHashMap(unittest.TestCase):
    def test_hash_map(self):
        #Test the basic functionality of the HashMap
        hm = HashMap()
        hm.add("value1")
        hm.add("value2")
        self.assertIn("value1", hm)
        self.assertIn("value2", hm)
        #Test the resizing functionality of the HashMap
        for i in range(100):
            hm.add(f"value{i}")
        self.assertTrue(hm._n_buckets == 128) #The number of buckets should have increased after adding 100 items
        #Test the resizing down functionality of the HashMap
        for i in range(100):
            hm.remove(f"value{i}")
        self.assertTrue(hm._n_buckets == 8) #The number of buckets should have decreased after removing 100 items
class TestEnrollment(unittest.TestCase):
    def test_enrollment(self):
        #Test the enrollment functionality of the Course class
        course = Course("CSE2050", 3, 50)
        course.prerequisite.add("CSE1010") #Add a prerequisite course to the course
        student1 = Student("STU12345", "Alice")
        student2 = Student("STU54321", "Bob")
        student1.enroll("CSE1010", "A") #This enroll function is essentially just adding the courses the student has enrolled and has grades in
        course.request_enroll(student1, "2024-09-01") #This should enroll successfully as the student meets the prerequisite
        course.request_enroll(student2, "2024-09-01") #This should not enroll successfully as the student does not meet the prerequisite
        self.assertIn(EnrollmentRecord(student1, "2024-09-01"), course.enrolled_roster) #Student 1 should be enrolled in the course
        self.assertNotIn(EnrollmentRecord(student2, "2024-09-01"), course.enrolled_roster) #Student 2 should not be enrolled in the course
class TestNewSort(unittest.TestCase):
    def test_sort_enrolled_new(self):
        #Test that enrolled_roster is sorted by different aspects in two new sorting methods.
        course = Course("CSE2050", 5, capacity=5) # I don't add prerequisites here because the sorting functions should work regardless of whether there are prerequisites or not, and it would just add unnecessary complexity to the test if we had to set up prerequisites and students that meet those prerequisites.
        students = [Student(student_id ="STU"+f"{i:05d}", name=f"Student{6-i}") for i in range(5, 0, -1)] #Create a reversed list of students to test sorting.
        #Testing student values:
        self.assertEqual(students[0].student_id, "STU00005")
        self.assertEqual(students[0].name, "Student1")
        self.assertEqual(students[4].student_id, "STU00001")
        self.assertEqual(students[4].name, "Student5")
        enrollment_dates = [datetime.date(2026, 4, i) for i in range(1, 6)] #Create a list of enrollment dates.
        for student, enroll_date in zip(students, enrollment_dates):
            course.request_enroll(student, enroll_date)
        #Test merge sort by name.
        course.sort_enrolled("name", "merge")
        self.assertEqual(course.enrolled_roster[0].student.name, "Student1")
        self.assertEqual(course.enrolled_roster[4].student.name, "Student5")
        #Test quick sort by enrollment date.
        course.sort_enrolled("date", "quick")
        self.assertEqual(course.enrolled_roster[0].enroll_date, datetime.date(2026, 4, 1))
        self.assertEqual(course.enrolled_roster[4].enroll_date, datetime.date(2026, 4, 5))
        #Test merge sort by student ID.
        course.sort_enrolled("id", "merge")
        self.assertEqual(course.enrolled_roster[0].student.student_id, "STU00001")
        self.assertEqual(course.enrolled_roster[4].student.student_id, "STU00005")
if __name__ == '__main__':
    unittest.main()
        