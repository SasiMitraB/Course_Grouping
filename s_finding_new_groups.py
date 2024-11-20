"""
Script to create Student and Course objects based on survey responses and interrelationship data.

The script:
1. Reads student email addresses and course preferences from a survey file.
2. Processes course interrelationships from a text file.
3. Creates Student and Course objects with detailed attributes.
4. Builds a mapping of course names to their indices for quick lookup.
"""
import pprint
import pandas as pd
from utils.obj import Student, Course

# Initialize lists for storing student and course objects
student_objects = []
ob_list = []  # List of Course objects

# Load student data from Excel
responses = pd.read_excel("filtered_feedback_form_responses.xlsx")
student_emails = responses['Email Address']
course_choices = responses['Courses that I plan to take in the upcoming semester']

# Create Student objects
for student_email, course_choice in zip(student_emails, course_choices):
    course_list = [course.strip() for course in course_choice.split(",")]
    student_objects.append(Student(student_email, course_list))

# Load course interrelationship data
with open("Course_interrelationships.txt", encoding='utf-8') as fhand:
    course_list_data = []
    temp_block = []
    for line in fhand:
        line = line.strip()
        if line:
            temp_block.append(line)
        else:
            if temp_block:
                course_list_data.append(temp_block)  # Changed to course_list_data
                temp_block = []
    if temp_block:  # Ensure the last block is added
        course_list_data.append(temp_block)  # Changed to course_list_data

# Process course data into Course objects
for course_block in course_list_data:  # Changed to course_list_data
    name = course_block[0].strip()
    index = int(course_block[1])
    relationships = {
        rel.split(":")[0].strip(): int(rel.split(":")[1])
        for rel in course_block[2:]
    }
    ob_list.append(Course(name, index, relationships))

# Build a course index mapping
course_index = {course.name: course.index for course in ob_list}

# Initialize a dictionary to hold the total number of students per course
course_totals = {}
for student in student_objects:
    for course in student.course_list:
        # Increment the course count for each student-course association
        course_totals[course] = course_totals.get(course, 0) + 1

# Sort courses based on the total number of students, from most to least
course_totals = dict(sorted(course_totals.items(), key=lambda item: item[1], reverse=True))

# Debug output to check the sorted course totals
print("\n\n\n")

# Set up initial groups with blank student lists
group = {f'Group {i}': [] for i in range(1, 12)}

# Courses to exclude from the grouping process
course_not_to_consider = [
    'BIO436/736 Experimental Biology Lab I 4', 
    'PHY415 Advanced Physics Lab III 4',
    'CHM335 Advanced Chem Lab - I 3', 
    'PHY345 Advanced Physics Lab II 3'
]

# Loop over courses and group them based on minimal conflicts
for course_name in course_totals.keys():
    # Skip courses that should not be considered
    if course_name in course_not_to_consider:
        continue

    # Retrieve the course object corresponding to the current course
    temp_course_object = ob_list[course_index[course_name] - 1]

    # Add the first course to Group 1 and the corresponding lovely object to Group 2
    if all(len(group[grp]) == 0 for grp in group):
        group["Group 1"].append(course_name)
        group["Group 2"].append(list(temp_course_object.lovely.keys())[0])
    else:
        # Check if the course is already accounted for in any group
        if any(course_name in grp for grp in group.values()):
            continue

        # Check for conflicts when adding the current course to the groups
        NO_OF_CONFLICTS = None
        GROUP_TO_ADD = None
        for gr in group.keys():
            test_group = group[gr].copy()  # Copy group to test for conflicts
            test_group.append(course_name)

            CONFLICTS = 0
            # Check how many students would have conflicts with this grouping
            for student in student_objects:
                if not student.check_if_single_group_works(test_group):
                    CONFLICTS += 1

            # Select the group with the fewest conflicts
            if NO_OF_CONFLICTS is None or CONFLICTS <= NO_OF_CONFLICTS:
                NO_OF_CONFLICTS = CONFLICTS
                GROUP_TO_ADD = gr

        # Add the course to the selected group with minimal conflicts
        group[GROUP_TO_ADD].append(course_name)

# Output the final groupings
pprint.pprint(group)
