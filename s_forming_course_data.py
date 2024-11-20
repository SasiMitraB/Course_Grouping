"""
Script for analyzing course preferences from a survey and saving the results in a structured JSON file.

This script performs the following tasks:
1. Reads student email addresses and their course preferences from an Excel file.
2. Cleans and filters the course preferences, excluding specific courses based on predefined criteria.
3. Creates Student objects with email and course list attributes.
4. Counts the total number of students enrolled in each course.
5. Analyzes relationships between courses by calculating how many students selected pairs of courses together.
6. Outputs the results in a JSON file with the following structure:
   - "course_counts": A dictionary mapping each course to the number of students enrolled.
   - "course_relationships": A nested dictionary where each course maps to another dictionary that shows co-selection counts with other courses.

Modules:
- pandas: For reading and processing the Excel data.
- json: For saving the output in a structured and human-readable format.

Classes:
- Student: Represents a student with an email and a list of selected courses.

Variables:
- responses (DataFrame): Contains the survey data from the Excel file.
- emails (Series): Extracted email addresses of the students.
- choices (Series): Extracted course preferences of the students.
- excluded_courses (set): A set of course names to be excluded from analysis.
- student_objects (list): A list to store all Student objects.
- course_counts (dict): A dictionary mapping courses to the number of students enrolled.
- course_relationships (dict): A dictionary mapping courses to their co-selection counts with other courses.

Output:
- The final analysis is saved as a JSON file (`s_course_interrelationship.json`) with a clear and structured format.

Usage:
1. Update the file path in `pd.read_excel()` with the actual path to the survey file.
2. Ensure that the `Student` class is implemented in `utils.obj` and provides attributes for `email` and `course_list`.
3. Run the script in a Python environment with access to the necessary dependencies.
"""
import json
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

# Process students and their courses
for email, course_string in zip(emails, choices):
    # Split, clean, and filter courses
    raw_courses = map(str.strip, course_string.split(","))
    course_list = [course for course in raw_courses if course not in excluded_courses]

    # Create Student object and add to the list
    student = Student(email, course_list)
    student_objects.append(student)

# Count total students enrolled in each course
course_counts = {}
for student in student_objects:
    for course in student.course_list:
        course_counts[course] = course_counts.get(course, 0) + 1

# Analyze relationships between courses
unique_courses = set(course_counts.keys())
course_relationships = {}

for course in unique_courses:
    related_courses = {
        other_course: sum(
            course in student.course_list and other_course in student.course_list
            for student in student_objects
        )
        for other_course in unique_courses if other_course != course
    }
    course_relationships[course] = related_courses

# Prepare the final output
output = {
    "course_counts": course_counts,
    "course_relationships": course_relationships,
}

# Save the output to a JSON file
OUTPUT_FILE = "s_course_interrelationships.json"
with open(OUTPUT_FILE, "w", encoding='utf-8') as file:
    json.dump(output, file, indent=4)

print(f"Analysis saved to {OUTPUT_FILE}")