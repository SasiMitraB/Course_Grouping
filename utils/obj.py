"""
Module: obj.py

This module defines classes to model students and courses in the course group, 
along with their relationships and properties. The classes include functionality for clash detection 
within proposed course groupings and maintaining course-student relationships.

Classes:
    - Student: Represents a student with their email, enrolled courses, and clash detection functionality.
    - Course: Represents a course, including its relationships with students and ranking based on intersection counts.

Classes:
    Student:
        - Attributes:
            email (str): The email of the student.
            course_list (list): List of courses the student is enrolled in.
            group_clash (bool): Indicates if there is a clash in proposed groupings.
            why_group_clash (list): Courses causing the group clash.
            which_group_clash (int): Index of the group causing the clash.
            single_group_course_clash (bool): Indicates a clash within a single proposed group.
            single_group_clash_courses (list): Courses causing the single group clash.

        - Methods:
            get_courses():
                Returns the list of courses the student is enrolled in.
            get_email():
                Returns the email of the student.
            check_if_group_works(proposed_grouping):
                Checks if a proposed grouping of courses works for the student. 
                Returns True if no clash, False otherwise.
            check_if_single_group_works(proposed_group):
                Checks if a single proposed group of courses works for the student. 
                Returns True if no clash, False otherwise.

    Course:
        - Attributes:
            name (str): The name of the course.
            love (dict): Dictionary of student-course intersections.
            lovely (dict): Sorted version of `love` based on intersection counts in descending order.
            index (int): Index of the course in the data.

        - Methods:
            No specific methods are defined for this class.
            
Usage:
    This module is intended for use in systems managing course enrollment and grouping processes. 
    The `Student` class allows for enrollment validation and clash detection, while the `Course` 
    class provides mechanisms to track and rank student-course relationships.

Examples:
    - Create a Student object:
        student = Student(email="student1@example.com", courses=["Math", "Physics"])

    - Check if a proposed grouping works:
        proposed_grouping = {"Group A": ["Math", "Biology"], "Group B": ["Physics", "Chemistry"]}
        is_group_valid = student.check_if_group_works(proposed_grouping)

    - Create a Course object:
        love_dict = {"student1@example.com": 2, "student2@example.com": 1}
        course = Course(name="Math", index=0, love=love_dict)
"""

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
