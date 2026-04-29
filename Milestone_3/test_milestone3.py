#Create tests for everything done in milestone 3, including the new HashMap implementation and the changes to the Course class. We will use the unittest framework for this.
#Developed by Mark Le
import unittest
from project1_2050 import *
import datetime
class TestHashMap(unittest.TestCase):
    def test_hash_map(self):
        #Test the basic functionality of the HashMap class, including adding, retrieving, and removing key-value pairs, as well as handling collisions and resizing.
        hashmap = HashMap()
        hashmap.put("CSE2050", ["CSE1010", "CSE1020"])
        hashmap.put("CSE1010", [])
        hashmap.put("CSE1020", [])
        self.assertEqual(hashmap.get("CSE2050"), ["CSE1010", "CSE1020"])
        self.assertEqual(hashmap.get("CSE1010"), [])
        self.assertEqual(hashmap.get("CSE1020"), [])
        with self.assertRaises(KeyError):
            hashmap.get("CSE9999") #Test that getting a non-existent key raises a KeyError
        hashmap.remove("CSE1020")
        with self.assertRaises(KeyError):
            hashmap.get("CSE1020") #Test that the removed key is no longer accessible

    def test_collision_handling(self): #Added by David Matos
        # Test that separate chaining correctly handles multiple keys that hash to the same bucket.
        hashmap = HashMap(size=2)
        keys = ["AAA", "BBB", "CCC", "DDD"]
        for k in keys:
            hashmap.put(k, f"value_{k}")
        for k in keys:
            self.assertEqual(hashmap.get(k), f"value_{k}")
        hashmap.remove("BBB")
        with self.assertRaises(KeyError):
            hashmap.get("BBB")
        self.assertEqual(hashmap.get("AAA"), "value_AAA")
        self.assertEqual(hashmap.get("CCC"), "value_CCC")
        self.assertEqual(hashmap.get("DDD"), "value_DDD")
 
    def test_rehashing(self): #Added by David Matos
        # Test that the table doubles when load factor reaches >= 0.8 and that every key is still accessible after the rehash.
        hashmap = HashMap()
        keys = [f"KEY{i:03d}" for i in range(10)]
        for k in keys:
            hashmap.put(k, f"val_{k}")
        self.assertEqual(len(hashmap), 10)
        for k in keys:
            self.assertEqual(hashmap.get(k), f"val_{k}")
        self.assertGreater(hashmap._n_buckets, 8)

class TestEnrollment(unittest.TestCase):
    def test_enrollment(self):
        #Test that students can enroll in a course, and that the enrollment records are created correctly with the correct enrollment dates. Also test that students who do not meet prerequisites cannot enroll.
        course = Course("CSE2600", 5, capacity=5) #Test a course with an empty prerequisite list first.
        student1 = Student(student_id="STU00001", name="Student1")
        student2 = Student(student_id="STU00002", name="Student2")
        student3 = Student(student_id="STU00003", name="Student3")
        student4 = Student(student_id="STU00004", name="Student4")
        student5 = Student(student_id="STU00005", name="Student5")
        #Test enrollment without prerequisites first, then we will add prerequisites and test that as well.
        course.request_enroll(student1, datetime.date(2026, 4, 1))
        course.request_enroll(student2, datetime.date(2026, 4, 2))
        course.request_enroll(student3, datetime.date(2026, 4, 3))
        course.request_enroll(student4, datetime.date(2026, 4, 4))
        course.request_enroll(student5, datetime.date(2026, 4, 5))
        self.assertEqual(len(course.enrolled_roster), 5)
        self.assertEqual(course.enrolled_roster[0].student.name, "Student1")
        self.assertEqual(course.enrolled_roster[0].enroll_date, datetime.date(2026, 4, 1))
        self.assertEqual(course.enrolled_roster[4].student.name, "Student5")
        self.assertEqual(course.enrolled_roster[4].enroll_date, datetime.date(2026, 4, 5))
        #Now test enrollment with prerequisites. We will use the same students and just add a prerequisite to the course, and then test that the students cannot enroll because they do not meet the prerequisite, and then we will add the prerequisite course to the students' studied courses and test that they can enroll successfully.
        course_with_prereq = Course("CSE2050", 5, capacity=5)
        prereq = Course("CSE1010", 5, capacity=5)
        student1.enroll(prereq, "A")
        student2.enroll(prereq, "B")
        student3.enroll(prereq, "C")
        student4.enroll(prereq, "D")
        course_with_prereq.request_enroll(student1, datetime.date(2026, 4, 1))
        course_with_prereq.request_enroll(student2, datetime.date(2026, 4, 2))
        course_with_prereq.request_enroll(student3, datetime.date(2026, 4, 3))
        course_with_prereq.request_enroll(student4, datetime.date(2026, 4, 4))
        course_with_prereq.request_enroll(student5, datetime.date(2026, 4, 5))
        self.assertEqual(len(course_with_prereq.enrolled_roster), 4) #Only 4 students should be enrolled because student5 does not meet the prerequisite
        self.assertEqual(course_with_prereq.enrolled_roster[0].student.name, "Student1")
        self.assertEqual(course_with_prereq.enrolled_roster[0].enroll_date, datetime.date(2026, 4, 1))
        self.assertEqual(course_with_prereq.enrolled_roster[3].student.name, "Student4")
        self.assertEqual(course_with_prereq.enrolled_roster[3].enroll_date, datetime.date(2026, 4, 4))  


class TestNewSort(unittest.TestCase):
    def test_sort_enrolled_new(self):
        #Test that enrolled_roster is sorted by different aspects in two new sorting methods.
        course = Course("CSE1010", 5, capacity=5) # I don't add courses with prerequisites here because the sorting functions should work regardless of whether there are prerequisites or not, and it would just add unnecessary complexity to the test if we had to set up prerequisites and students that meet those prerequisites.
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
        