"""
Haven't decided and implemented any of these yet.
"""
import json
from obj import Student
import pandas as pd

#TODO: Work in progress
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

        #TODO: some issue with the class need to get back
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
