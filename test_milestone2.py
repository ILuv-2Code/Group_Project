#Developed by Mark Le, milestone 2.
import unittest
import datetime
from project1_2050 import *
class TestMilestone2(unittest.TestCase):
    #Test the new functions added in milestone 2.
    def test_linked_queue(self):
        #Test FIFO behavior of LinkedQueue.
        queue = LinkedQueue()
        for i in range(5):
            queue.enqueue(i)
        for i in range(5):
            self.assertEqual(queue.dequeue(), i)
        #Test dequeue on empty raises
        with self.assertRaises(ValueError):
            queue.dequeue()
        #Test size tracking.
        for i in range(3):
            queue.enqueue(i)
        self.assertEqual(queue.size, 3)
        queue.dequeue()
        self.assertEqual(queue.size, 2)
    def test_enrollment(self):
        #Test request_enrollment in project1_2050.
        course = Course("CSE2050", 3, capacity=1) #Set capacity to 1 for testing.
        student1 = Student("STU12345", "Alice Smith")
        student2 = Student("STU67890", "Bob Johnson")
        #Test successful enrollment.
        course.request_enroll(student1, datetime.date(2026, 4, 1))
        self.assertEqual(len(course.enrolled_roster), 1)
        self.assertEqual(course.enrolled_roster[0].student, student1)
        #Test waitlist enrollment when course is full.
        course.request_enroll(student2, datetime.date(2026, 4, 2))
        self.assertEqual(course.waitlist.size, 1)
        self.assertEqual(course.waitlist_roster[0], student2)
        self.assertNotIn(student2, [record.student for record in course.enrolled_roster]) # Ensure student2 is not enrolled.
        #Test remove_waitlist function.
        course.capacity = 2 # Increase capacity to allow enrollment from waitlist.
        course.request_enroll(student2, datetime.date(2026, 4, 2)) # Try to enroll student2 again, should move from waitlist to enrolled.
        self.assertEqual(len(course.enrolled_roster), 2)
        self.assertIn(student2, [record.student for record in course.enrolled_roster])
        self.assertEqual(course.waitlist.size, 0)
        self.assertEqual(len(course.waitlist_roster), 0)
        #Test drop function and replacement from waitlist.
        student3 = Student("STU54321", "Charlie Brown")
        course.request_enroll(student3, datetime.date(2026, 4, 3)) # Add student3 to waitlist.
        course.drop(student1.student_id, datetime.date(2026, 4, 4)) # Drop student1, should enroll student3 from wait
        self.assertEqual(len(course.enrolled_roster), 2)
        self.assertIn(student3, [record.student for record in course.enrolled_roster])
        self.assertEqual(course.waitlist.size, 0)
        self.assertEqual(len(course.waitlist_roster), 0)
    def test_sorted_enrollment(self):
        #Test that enrolled_roster is sorted by enrollment date.
        course = Course("CSE2050", 5, capacity=5)
        students = [Student(student_id ="STU"+f"{i:05d}", name=f"Student{i}") for i in range(5, 0, -1)] #Create a reversed list of students to test sorting.
        #Testing student values:
        self.assertEqual(students[0].student_id, "STU00005")
        self.assertEqual(students[0].name, "Student5")
        self.assertEqual(students[4].student_id, "STU00001")
        self.assertEqual(students[4].name, "Student1")
        enrollment_dates = [datetime.date(2026, 4, i) for i in range(1, 6)] #Create a list of enrollment dates.
        for student, enroll_date in zip(students, enrollment_dates):
            course.request_enroll(student, enroll_date)
        #Test bubble sort by enrollment date.
        course.sort_enrolled('date', 'bubble')
        for i in range(1, 6):
            self.assertEqual(course.enrolled_roster[i-1].enroll_date, datetime.date(2026, 4, i))
        #Test selection sort by name:
        course.sort_enrolled('name', 'selection')
        for i in range(1, 6):
            self.assertEqual(course.enrolled_roster[i-1].student.name, f"Student{i}")
        #Test insertion sort by student ID:
        course.sort_enrolled('id', 'insertion')
        for i in range(1, 6):
            self.assertEqual(course.enrolled_roster[i-1].student.student_id, f"STU{(i):05d}")
    def test_binary_search(self):
        #Test binary search for enrolled students.
        course = Course("CSE2050", 5, capacity=5)
        students = [Student(student_id ="STU"+f"{i:05d}", name=f"Student{i}") for i in range(1, 6)]
        enrollment_dates = [datetime.date(2026, 4, i) for i in range(1, 6)]
        for student, enroll_date in zip(students, enrollment_dates):
            course.request_enroll(student, enroll_date)
        #Ensure roster is sorted by student ID for binary search.
        course.sort_enrolled('id', 'insertion')
        #Test finding existing students.
        for student in students:
            found_index = recursive_binary_search(course.enrolled_roster, student.student_id, 0, len(course.enrolled_roster)-1)
            self.assertIsNotNone(found_index)
            self.assertEqual(course.enrolled_roster[found_index], course.enrolled_roster[students.index(student)])
        #Test searching for non-existent student.
        self.assertEqual(recursive_binary_search(course.enrolled_roster, "STU99999", 0, len(course.enrolled_roster)-1), -1)
if __name__ == '__main__':
    unittest.main()