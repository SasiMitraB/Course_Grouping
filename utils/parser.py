import pandas as pd
from .obj import Student
def excel_parsing(response_file: str, email_col_num: int, course_list_col_num: int, excluded_courses: set) -> list | dict:
    #TODO: Maybe we can implement a process where it counts the number of credits which can be added as an additional attribute in Student class and can be used for future processing.
    """
    Read the Excel file containing the survey responses and extract the email addresses and course preferences and processes them into .
    """
    student_objects = []
    # Read the Excel file using pandas
    responses = pd.read_excel(response_file)
    
    # Extract email addresses and course preferences
    emails = responses.iloc[:, email_col_num]
    choices = responses.iloc[:, course_list_col_num]

    
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
    return student_objects, course_counts