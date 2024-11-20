"""
Script for processing course preferences and relationships to create groupings with minimal conflicts.

This script performs the following tasks:
1. Reads student email addresses and their course preferences from an Excel file.
2. Processes course interrelationship data from a JSON file (generated from a previous script).
3. Creates Student and Course objects with attributes for email, course list, and relationships.
4. Builds groups of courses while minimizing conflicts based on student preferences and course relationships.
5. Outputs the final groupings to a JSON file.

Key Features:
- Accepts course interrelationship data as a JSON input for improved flexibility and clarity.
- Dynamically adjusts course groupings to minimize conflicts among students.
- Excludes certain predefined courses from grouping.
- Provides detailed outputs for debugging and analysis.

Modules:
- `pandas`: For reading and processing survey data from Excel files.
- `json`: For loading interrelationship data and saving the output.
- `pprint`: For neatly printing the final course groupings.
- `utils.obj`: For `Student` and `Course` classes with relevant methods.

Inputs:
1. `Course_preference_survey_(Responses).xlsx` (Excel file): Contains student email addresses and their course preferences.
2. `s_course_interrelationships.json` (JSON file): Contains course names, indices, and interrelationship data.

Outputs:
1. Groupings of courses saved in `s_course_groupings.json`.
2. Debugging information printed in the console.

Usage:
1. Ensure the input Excel file and JSON file are available in the working directory.
2. Update the script paths (`pd.read_excel` and `open`) if needed.
3. Run the script in a Python environment with necessary dependencies.
"""
import pprint
import json
import pandas as pd
from utils.obj import Student, Course


# Load data from the JSON file
with open("s_course_relationships.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Parse course data
course_objects = [
    Course(course["name"], course["index"], course["related_courses"])
    for course in data["course_relationships"]
]
course_index = {course["name"]: course["index"] for course in data["course_relationships"]}

# Parse student data (assuming preprocessed list of students)
student_objects = []
responses = pd.read_excel("Course_preference_survey_(Responses).xlsx")
student_emails = responses['Email Address']
course_choices = responses['What are all the courses you would like to take in Monsoon 2022? (choose courses worth 18-25 credits only)']

for email, course_choice in zip(student_emails, course_choices):
    course_list = [course.strip() for course in course_choice.split(",")]
    student_objects.append(Student(email, course_list))

# Initialize groups
group = {f'Group {i}': [] for i in range(1, 12)}
excluded_courses = [
    'BIO436/736 Experimental Biology Lab I 4',
    'PHY415 Advanced Physics Lab III 4',
    'CHM335 Advanced Chem Lab - I 3',
    'PHY345 Advanced Physics Lab II 3'
]

# Group courses based on conflicts
for course_name in data["course_counts"].keys():
    if course_name in excluded_courses:
        continue

    course_obj = course_objects[course_index[course_name] - 1]

    # Assign the course to the first group initially
    if all(len(group[grp]) == 0 for grp in group):
        group["Group 1"].append(course_name)
        group["Group 2"].append(list(course_obj.lovely.keys())[0])
    else:
        if any(course_name in grp for grp in group.values()):
            continue

        NO_OF_CONFLICTS = None
        GROUP_TO_ADD = None

        for gr in group.keys():
            test_group = group[gr].copy()
            test_group.append(course_name)

            CONFLICTS = sum(
                not student.check_if_single_group_works(test_group)
                for student in student_objects
            )

            if NO_OF_CONFLICTS is None or CONFLICTS <= NO_OF_CONFLICTS:
                NO_OF_CONFLICTS = CONFLICTS
                GROUP_TO_ADD = gr

        group[GROUP_TO_ADD].append(course_name)

# Save final groupings to a JSON file
with open("s_course_groups.json", "w", encoding="utf-8") as f:
    json.dump(group, f, indent=4)

print("Course groups saved to s_course_groups.json.")

# 1. Calculating the number of students who agree with the grouping
result = [student.check_if_group_works(group) for student in student_objects]
metric = sum(result)

print("The total amount of students who gave input are " + str(len(student_objects)))
print("The total amount of people agreeing with this grouping is " + str(metric))

# 2. Identifying students with clashes
clashed_groups = {}
print("\nStudents with clashes:")
for student in student_objects:
    if student.group_clash:
        print(f"Email: {student.email}")
        print(f"Reasons for clash: {student.why_group_clash}")
        print(f"Groups clashing: {student.which_group_clash}")
        print()
        for course in student.why_group_clash:
            clashed_groups[course] = clashed_groups.get(course, 0) + 1

# 3. Counting the total number of courses in the grouping
total_courses = sum(len(group[g]) for g in group.keys())
print("The total number of courses in the grouping is " + str(total_courses))

# Debugging: Print the clashed courses and their frequencies
print("\nClashed groups and frequencies:")
pprint.pprint(clashed_groups)

# Print and save the final groupings
print("\nFinal groupings:")
pprint.pprint(group)
