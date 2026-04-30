from project1_2050 import *
import csv
import datetime
import random

# Demo Script Developed by David Matos and Mark Le
# Runs all demos for milestone 1-3
with open('demo_output.txt', 'w') as f:
    # Redirect print statements to the file
    import sys
    sys.stdout = f
    # demo 1
    print("---------------------Running Demo 1---------------------")
    print("Demonstation: University Course and Student Management System")
    print("-------------------------------------------------------------")
    UConn = University() #Initializes University object
    with open('course_catalog.csv', 'r') as f: # Reads course catalog and adds courses to UConn
        course_reader = csv.reader(f, delimiter=',')
        next(course_reader) # skip header row
        for row in course_reader:
            course_code, credits = row
            UConn.add_course(course_code, int(credits), 30) # Milestone 3: capacity added (default 30); course_catalog.csv has no capacity column
    with open('university_data.csv', 'r') as f: # Reads student enrollments and adds students (name + id) and their course enrollments to UConn (TODO: Do we need to change for Milestone 3?)
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
    print("Print GPA of a student")
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
    print("Print all the courses and course info ( grades and credits ) for a student")
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
    print("Calculate mean and median for the GPA of all students in the university")
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
    print("Print common students in two different courses:")
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
    print("\n---------------------Finished Demo 1---------------------")

    # demo 2
    print("---------------------Running Demo 2---------------------")
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
    courses = [c for c in courses if c.course_code not in PREREQUISITE or not PREREQUISITE.get(c.course_code)]
    print("Courses loaded (filtered to those with no prerequisites):")
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
    
    print("\nDemo 2.2: Performing binary search for a student in each course...")
    for course in courses:
        if course.enrolled_roster:
            course.sort_enrolled("id", "merge")
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
            
    print("\n---------------------Finished Demo 2---------------------")

    # demo 3
    print("\n---------------------Running Demo 3---------------------")
    print("\n---------------------------Hash Map---------------------------")
    
    hm = HashMap(size=5)
    print("Buckets before rehash:", hm._n_buckets)
    hm.put("CSE1010", [])
    hm.put("CSE2050", ["CSE1010"])
    hm.put("CSE2100", ["CSE2050"])
    hm.put("CSE3100", ["CSE2050", "CSE2100"])
    
    print(hm.get("CSE2050"))
    print(hm.get("CSE3100"))
    
    hm.put("CSE4001", ["CSE3100"])
    print("Buckets after rehash:", hm._n_buckets)
    
    print("CSE2050" in hm)
    print("CSE9999" in hm)
    
    try:
        hm.put("CSE2050", ["something"])
    except KeyError as e:
        print(e)
    
    try:
        hm.get("CSE9999")
    except KeyError as e:
        print(e)
    
    print("\n---------------------------Pre-req. verification---------------------------")
    
    uni = University()
    
    adv_course_code = None
    adv_prereqs = []
    
    for key, value in PREREQUISITE:
        if value:
            adv_course_code = key
            adv_prereqs = value
            break
    
    print("Advanced course:", adv_course_code)
    print("Its prerequisites:", adv_prereqs)
    
    adv = uni.add_course(adv_course_code, 3, 10)
    
    alice = uni.add_student("STU00001", "Alice")
    bob   = uni.add_student("STU00002", "Bob")
    
    for prereq_code in adv_prereqs:
        prereq_course = uni.add_course(prereq_code, 3, 10)
        alice.enroll(prereq_course, "A")
    
    print("Alice's completed courses:", [c.course_code for c in alice.get_courses()])
    print("Bob's completed courses:  ", [c.course_code for c in bob.get_courses()])
    

    adv.request_enroll(alice, datetime.date(2026, 1, 15))
    print("Enrolled in", adv_course_code, ":", [r.student.name for r in adv.enrolled_roster])

    # prints warning instead of error
    adv.request_enroll(bob, datetime.date(2026, 1, 15))

    
    print("\n---------------------------Sorting---------------------------")
    
    sort_course = uni.add_course("CSE9001", 3, 20)
    
    students_data = [
        ("STU00010", "Zara",  datetime.date(2026, 3, 5)),
        ("STU00011", "Alice", datetime.date(2026, 1, 10)),
        ("STU00012", "Mark",  datetime.date(2026, 2, 20)),
        ("STU00013", "Bob",   datetime.date(2026, 1, 5)),
        ("STU00014", "Yara",  datetime.date(2026, 3, 1)),
    ]
    
    for sid, sname, sdate in students_data:
        s = uni.add_student(sid, sname)
        sort_course.request_enroll(s, sdate)
    
    print("Original order:")
    for r in sort_course.enrolled_roster:
        print(" ", r.student.student_id, r.student.name, r.enroll_date)
    
    sort_course.sort_enrolled("name", "merge")
    print("\nMerge sort by name:")
    for r in sort_course.enrolled_roster:
        print(" ", r.student.student_id, r.student.name, r.enroll_date)
    
    sort_course.sort_enrolled("id", "quick")
    print("\nQuick sort by id:")
    for r in sort_course.enrolled_roster:
        print(" ", r.student.student_id, r.student.name, r.enroll_date)
    
    sort_course.sort_enrolled("date", "merge")
    print("\nMerge sort by date:")
    for r in sort_course.enrolled_roster:
        print(" ", r.student.student_id, r.student.name, r.enroll_date)

    print("---------------------Finished Demo 3---------------------")