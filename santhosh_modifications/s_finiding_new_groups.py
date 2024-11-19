"""
Script to create Student and Course objects based on survey responses and interrelationship data.

The script:
1. Reads student email addresses and course preferences from a survey file.
2. Processes course interrelationships from a text file.
3. Creates Student and Course objects with detailed attributes.
4. Builds a mapping of course names to their indices for quick lookup.
"""
import json
import pprint
import pandas as pd


class Student:
    """
    Represents a student with properties related to course enrollment and clash detection.

    Attributes:
        email (str): The email of the student.
        course_list (list): List of courses the student is enrolled in.
        group_clash (bool): Indicates if there is a clash in proposed groupings.
        why_group_clash (list): Courses causing the group clash.
        which_group_clash (int): Index of the group causing the clash.
        single_group_course_clash (bool): Indicates a clash within a single proposed group.
        single_group_clash_courses (list): Courses causing the single group clash.
    """

    def __init__(self, email, courses):
        self.email = email
        self.course_list = courses
        self.group_clash = False
        self.why_group_clash = None
        self.which_group_clash = None
        self.single_group_course_clash = False
        self.single_group_clash_courses = None

    def get_courses(self):
        """Returns the list of courses the student is enrolled in."""
        return self.course_list

    def get_email(self):
        """Returns the email of the student."""
        return self.email

    def check_if_group_works(self, proposed_grouping):
        """
        Checks if a proposed grouping of courses works for the student.

        Args:
            proposed_grouping (dict):
            Dictionary where keys are group names and values are lists of courses.

        Returns:
            bool: True if no clash, False otherwise.
        """
        for group_index, courses in enumerate(proposed_grouping.values()):
            intersection = set(courses).intersection(self.course_list)
            if len(intersection) > 1:
                self.group_clash = True
                self.why_group_clash = list(intersection)
                self.which_group_clash = group_index
                return False

        self.group_clash = False
        self.why_group_clash = None
        self.which_group_clash = None
        return True

    def check_if_single_group_works(self, proposed_group):
        """
        Checks if a single proposed group of courses works for the student.

        Args:
            proposed_group (list): List of courses in the proposed group.

        Returns:
            bool: True if no clash, False otherwise.
        """
        intersection = set(proposed_group).intersection(self.course_list)
        if len(intersection) > 1:
            self.single_group_course_clash = True
            self.single_group_clash_courses = list(intersection)
            return False

        self.single_group_course_clash = False
        self.single_group_clash_courses = None
        return True


class Course:
    """
    Represents a course with properties to manage relationships with students.

    Attributes:
        name (str): The name of the course.
        love (dict): Dictionary of student-course intersections.
        lovely (dict): Sorted version of `love` based on intersection counts in descending order.
        index (int): Index of the course in the data.
    """

    def __init__(self, name, index, love):
        self.name = name
        self.love = love
        self.lovely = dict(sorted(self.love.items(), key=lambda item: item[1], reverse=True))
        self.index = index


# TODO: Work in progress
def excel_to_json(file_path):
    """
    Reads student-course data from an Excel file, processes it, and outputs a JSON file.

    Args:
        file_path (str): Path to the input Excel file.

    Returns:
        str: JSON-formatted string of processed student and course data.
    """
    # Read data from Excel
    df = pd.read_excel(file_path)

    # Validate input structure
    if not {'Email', 'Courses'}.issubset(df.columns):
        raise ValueError("Excel file must contain 'Email' and 'Courses' columns.")

    students = []
    courses = {}

    for _, row in df.iterrows():
        student_email = row['Email']  # Changed to student_email
        course_list = row['Courses'].split(',')  # Assuming courses are comma-separated

        # Create a Student object
        student = Student(student_email, course_list)
        students.append(student)

        # TODO: some issue with the class need to get back
        # # Update Course data
        # for course in course_list:
        #     if course not in courses:
        #         courses[course] = Course(course)

    # Generate JSON output
    output = {
        "students": [
            {
                "email": student.get_email(),
                "courses": student.get_courses()
            } for student in students
        ],
        "courses": [
            {
                "name": course.name,
                "lovely": course.lovely
            } for course in courses.values()
        ]
    }

    # Write to JSON file
    output_file = "output.json"
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(output, f, indent=4)

    return json.dumps(output, indent=4)

# Initialize lists for storing student and course objects
student_objects = []
ob_list = []  # List of Course objects

# Load student data from Excel
responses = pd.read_excel("filtered_feedback_form_responses.xlsx")
student_emails = responses['Email Address']  # Changed to student_emails
course_choices = responses['Courses that I plan to take in the upcoming semester']  # Changed to course_choices

# Create Student objects
for student_email, course_choice in zip(student_emails, course_choices):
    course_list = [course.strip() for course in course_choice.split(",")]
    student_objects.append(Student(student_email, course_list))

# Load course interrelationship data
with open("Course_interrelationships.txt", encoding='utf-8') as fhand:
    course_list_data = []  # Changed to course_list_data
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