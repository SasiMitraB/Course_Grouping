"""
Script to create Student and Course objects based on survey responses and creates the interrelationship data.

The script:
1. Reads student email addresses and course preferences from a survey file.
2. Creates Student objects with detailed attributes.
3. Builds a mapping of course names to their indices for quick lookup.
"""
import pandas as pd
from utils.obj import Student

# Read responses from Excel
responses = pd.read_excel("Course_preference_survey_(Responses).xlsx")
emails = responses['Email Address']
choices = responses['What are all the courses you would like to take in Monsoon 2022? (choose courses worth 18-25 credits only)']

# Define a set of courses to exclude from analysis
excluded_courses = {"BIO339/639", "BIO416/716"}

# Create a list to store all student objects
student_objects = []

# Iterate over each email and corresponding course choices
for email, course_string in zip(emails, choices):
    # Split the course string into individual courses
    raw_courses = course_string.split(",")
    
    # Clean and filter the courses, removing extra spaces and excluded courses
    course_list = []
    for course in raw_courses:
        cleaned_course = course.strip()  # Remove leading and trailing spaces
        if cleaned_course not in excluded_courses:  # Exclude certain courses
            course_list.append(cleaned_course)

    # Create a new Student object and add it to the list
    student = Student(email, course_list)
    student_objects.append(student)

# Count the total number of students enrolled in each course
course_counts = {}
for student in student_objects:
    for course in student.course_list:
        if course not in course_counts:
            course_counts[course] = 0
        course_counts[course] += 1  # Increment the count for this course

# Print the total counts for each course
print("Course counts:")
print(course_counts)
print("\n")

# Identify all unique courses from the data
unique_courses = set(course_counts.keys())

# Analyze and print relationships between courses
INDEX = 1  # Index to keep track of course number
for course in unique_courses:
    # Initialize a dictionary to store relationships for the current course
    related_courses = {}

    # Compare the current course with all other courses
    for other_course in unique_courses:
        if other_course == course:
            continue  # Skip comparing the course with itself
        
        # Count how many students selected both the current course and the other course
        co_selection_count = 0
        for student in student_objects:
            if course in student.course_list and other_course in student.course_list:
                co_selection_count += 1
        
        # Store the co-selection count for the other course
        related_courses[other_course] = co_selection_count

    # Print the relationships for the current course
    print(f"Course: {course} (Index: {INDEX})")
    print(related_courses)
    print("\n")
    INDEX += 1