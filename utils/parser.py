"""
This module provides functionality to parse any file and its sole purpose streamline the parsing, for time being I have only implemented to parse excel file from student response and convert them into student objects with other detailed information .

Functions:
    excel_parsing(response_file: str, email_col_num: int, course_list_col_num: int, excluded_courses: set) -> list | dict:
        Parses an Excel file to generate Student objects and count course enrollments.

Usage:
    1. Import this module to handle parsing of student responses from an Excel file for further processing.
"""
import pandas as pd
from .obj import Student

def excel_parsing(response_file: str, email_col_num: int, course_list_col_num: int, excluded_courses: set) -> list | dict:
    """
    Parses an Excel file to extract student email addresses and their course preferences, 
    creates Student objects, and calculates the total number of enrollments for each course.

    Args:
        response_file (str): Path to the Excel file containing student responses.
        email_col_num (int): Column number (zero-indexed) for email addresses.
        course_list_col_num (int): Column number (zero-indexed) for course preferences (comma-separated).
        excluded_courses (set): A set of course names to exclude from the parsed data.

    Returns:
        list: A list of Student objects, each containing an email and a list of preferred courses.
        dict: A dictionary with course names as keys and their respective enrollment counts as values.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If there are issues with the format of the input file or column indices.

    Notes:
        - Courses in the preferences column are expected to be comma-separated strings.
        - Excluded courses are not included in the `Student` objects or the course count.
    """
    student_objects = []

    try:
        responses = pd.read_excel(response_file)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"The file '{response_file}' was not found.") from exc
    except Exception as exc:
        raise ValueError(f"An error occurred while reading the Excel file: {exc}") from exc

    try:
        emails = responses.iloc[:, email_col_num]
        choices = responses.iloc[:, course_list_col_num]
    except IndexError as exc:
        raise ValueError("The provided column indices are out of range for the input file.") from exc

    for email, course_string in zip(emails, choices):
        if pd.isna(email) or pd.isna(course_string):
            continue

        raw_courses = course_string.split(",")
        course_list = [
            course.strip()
            for course in raw_courses
            if course.strip() and course.strip() not in excluded_courses
        ]

        student = Student(email, course_list)
        student_objects.append(student)

    course_counts = {}
    for student in student_objects:
        for course in student.course_list:
            if course not in course_counts:
                course_counts[course] = 0
            course_counts[course] += 1

    return student_objects, course_counts
