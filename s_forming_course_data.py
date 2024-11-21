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
from utils.parser import excel_parsing

# Excel file location
EXCEL_FILE = "Course_preference_survey_(Responses).xlsx"

# Read responses from Excel
responses = pd.read_excel(EXCEL_FILE)
emails = responses['Email Address']
choices = responses['What are all the courses you would like to take in Monsoon 2022? (choose courses worth 18-25 credits only)']

# Define a set of courses to exclude from analysis
excluded_courses = {"BIO339/639", "BIO416/716"}

student_objects, course_counts = excel_parsing(EXCEL_FILE, 1, 2, excluded_courses)

# Generate unique indices for courses
course_index = {}
current_index = 1

for course in course_counts.keys():
    course_index[course] = current_index
    current_index += 1

# Analyze relationships between courses
relationships = {}
for course in course_counts.keys():
    related_courses = {}
    for other_course in course_counts.keys():
        if other_course == course:
            continue
        
        # Count co-selection
        co_selection_count = sum(
            course in student.course_list and other_course in student.course_list
            for student in student_objects
        )
        related_courses[other_course] = co_selection_count

    relationships[course] = related_courses

# Prepare data for JSON output
course_relationships = []
for course_name, total_students in course_counts.items():
    course_relationships.append({
        "name": course_name,
        "index": course_index[course_name],
        "total_students": total_students,
        "related_courses": relationships[course_name]
    })

output_data = {
    "course_counts": course_counts,
    "course_relationships": course_relationships
}

# Write the output to a JSON file
with open("s_course_relationships.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=4)

print("Course relationships saved to course_relationships.json.")