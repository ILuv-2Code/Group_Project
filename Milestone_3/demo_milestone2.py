from project1_2050 import *
import csv
import datetime
import random
#Presented are the demos added in Milestone 2, by Mark Le
if __name__ == "__main__":
    print("Demo Milestone 2: Enroll, Waitlist, Sorting, Dropping")
    print("*" * 50)
    print("Generate UConn Universtity Object")
    uconn = University()
    print("Updating data from course_catalog_CSE10_with_capacity.csv...")
    with open("course_catalog_CSE10_with_capacity.csv", mode='r') as file:
        reader = csv.DictReader(file)
        print("Loading courses from CSV:")
        print("Note: We're not taking the name of the course because the Course class doesn't have a name attribute, but we will load the course code, credits, and capacity.")
        for row in reader:
            course_code = row['course_id']
            credits = int(row['credits'])
            capacity = int(row['capacity'])
            print(f"Loading course: {course_code} with {credits} credits and capacity of {capacity}")
            uconn.add_course(course_code, credits, capacity)
    courses = list(uconn.courses.values()) 
    print("Courses loaded:")    
    for course in courses:
        print(f"{course.course_code} - Credits: {course.credits}, Capacity: {course.capacity}")
    print("\nCreating students and enrolling in all classes...")
    print("Grabbing data from enrollments_CSE10.csv...")
    FIRST_NAMES = ["Liam", "Olivia", "Noah", "Emma", "Ava", "Sophia", "Isabella", "Mason", "Lucas", "Mia"]
    LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Martinez", "Hernandez"]
    with open("enrollments_CSE10.csv", mode='r') as file:
        reader = csv.DictReader(file)
        students = {}
        for row in reader:
            student_id = row['student_id']
            name = random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES) # Generate a random name for demonstration purposes. This is not linked to university_data.csv as they have different enrollment statuses. Therefore, we only use this demo as a way to test the enrollment, waitlist, sorting, and dropping functionalities with a larger dataset.
            course_code = row['course_id'] #We're currently not using term and attempt for this demo, but it maybe useful in future demos.
            if student_id not in students:
                students[student_id] = Student(student_id, name)
            student = students[student_id]
            course = next((c for c in courses if c.course_code == course_code), None)
            if course:
                course.request_enroll(student, datetime.date(2026, 1, random.randint(1, 31))) # Using a random date in January to check sorting algorithm.
    print("Enrollment complete. Displaying enrolled students for each course:")
    for course in courses:
        print(f"\n{course.course_code} Enrolled Students:")
        for record in course.enrolled_roster:
            print(f"{record.student.student_id} - {record.student.name} (Enrolled on: {record.enroll_date})")
    print("\nDisplaying waitlisted students for each course:")
    for course in courses:
        print(f"\n{course.course_code} Waitlisted Students:")
        for student in course.waitlist_roster:
            print(f"{student.student_id} - {student.name}")
    print("\nDemo 2.1: Sorting enrolled students by enrollment date for each course using different sorting algorithms...")
    index = 0
    methods = ["bubble", "selection", "insertion"]
    sort_by = ["date", "name", "id"]
    for course in courses:
        course.sort_enrolled(sort_by[index % 3], methods[index % 3])
        index += 1
    print("Sorting complete. Displaying sorted enrolled students for each course:")
    index = 0 #Reset index to display sorted students in the same order as before.
    for course in courses:
        print(f"\n{course.course_code} Enrolled Students based on {sort_by[index % 3]} using ({methods[index % 3]} sort):")
        for record in course.enrolled_roster:
            print(f"{record.student.student_id} - {record.student.name} (Enrolled on: {record.enroll_date})")
        index += 1
        print("\n") #Add a newline for better readability between courses.
    print("\nDemo 2.2:Performing binary search for a student in each course...")
    for course in courses:
        if course.enrolled_roster:
            target_student = course.enrolled_roster[len(course.enrolled_roster) // 2].student # Search for the middle student for demonstration purposes.
            print(f"Searching for {target_student.student_id} - {target_student.name} in {course.course_code}...")
            found_record = recursive_binary_search(course.enrolled_roster, target_student.student_id, 0, len(course.enrolled_roster)-1)
            if found_record:
                found_student = course.enrolled_roster[found_record].student
                print(f"Found: {found_student.student_id} - {found_student.name} (Enrolled on: {course.enrolled_roster[found_record].enroll_date})")
            else:
                print("Student not found in enrolled roster.")
        else:
            print(f"No enrolled students in {course.course_code} to search for.")    
    print("\nDropping a student from each course and checking waitlist replacement...")
    for course in courses:
        if course.enrolled_roster:
            student_to_drop = course.enrolled_roster[0].student # Drop the first enrolled student for demonstration.
            print(f"Dropping {student_to_drop.student_id} - {student_to_drop.name} from {course.course_code}...")
            prev_len_enrolled = len(course.enrolled_roster)
            course.drop(student_to_drop.student_id, datetime.date(2026, 2, 1)) # Using a fixed date for dropping.
            if len(course.enrolled_roster) < prev_len_enrolled:
                print(f"\nNo student was enrolled from the waitlist.")
            else:
                print(f"\nThe new enrolled student from the waitlist is: {course.enrolled_roster[-1].student.name}, studentID {course.enrolled_roster[-1].student.student_id}")
            print(f"After dropping, enrolled students in {course.course_code}:")
            for record in course.enrolled_roster:
                print(f"{record.student.student_id} - {record.student.name} (Enrolled on: {record.enroll_date})")
            print(f"Waitlisted students in {course.course_code}:")
            for student in course.waitlist_roster:
                print(f"{student.student_id} - {student.name}")
            print("\n") #Add a newline for better readability between courses.
    print("\nDemo Milestone 2 complete.")