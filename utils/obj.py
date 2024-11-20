"""
This module consists of object classes where all the items can be accessed through dynamic classes.
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
