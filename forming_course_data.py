import numpy as np
import pandas as pd
import pprint
import random

''' Set up a student class to easily edit student related properties'''
class Student:
    def __init__(self,email,courses):
        self.course_list = courses #Courses stored as a list/set
        self.email = email         #Email just because having it stored would be nice
        self.groupClash = False    #We have a method which accepts a grouping and changes this variable if the grouping clashes with the student's
                                   #Desired choice of courses
        self.whyGroupClash = None  #The method also changes this varible to which courses are causing the problem
        self.whichGroupClash = None #This variables tells us which group is causing the problem in the grouping

        self.SingleGroupCourseClash = False             #We have made a method which checks clashes in a single group
        self.SingleGroupCourseClashCourse = None        #These 2 varibles help in that sense

    def getCourses(self):                               #Method to help get courses
        return self.course_list
    def getEmail(self):                                 #Method to help get email
        return self.email

    ''' Main method which accepts a proposed grouping in the form of a dictionary'''
    def checkIfWorks(self,proposed_grouping):
        for i in proposed_grouping.values():            #The values of the dictionary are lists which have the courses in one group
            if len(set(i).intersection(self.course_list))>1:  #We say there's a clash when the intersection of a group and a course list is more than 1
                self.groupClash = True
                self.whyGroupClash = list(set(i).intersection(set(self.course_list)))           #Sets variables to data that we would like to have
                self.whichGroupClash = list(proposed_grouping.values()).index(i)
                return False                                                                    #Note down first clash and then stop
            else:
                self.groupClash=False
                self.whyGroupClash=None                                         #In case nothing happens we keep going with the next group
                self.whichGroupClash=None
                continue
        return True                                                             #Only returns True if there are no clashes

    ''' The single group form of the previous Main method which accepts a proposed group in the form of a list'''
    def checkIfWorksOneGroup(self,proposed_group):
        if len(set(proposed_group).intersection(self.course_list))>1:
            self.SingleGroupCourseClash = list(set(proposed_group).intersection(self.course_list))
            self.SingleGroupCourseClashCourse = True
            return False
        else:                                                                   #same logic is applicable
            self.SingleGroupCourseClash = None
            self.SingleGroupCourseClashCourse = False
            return True

''' Set up a Course Class to keep track of course related properties'''
class Course:
    def __init__(self, name , index, love):
        self.name = name        #Name of the course
        self.love = love        #love attribute is the course in which there are the most number of intersection of students with this course as well
        self.lovely = dict(sorted(self.love.items(), key = lambda item: item[1],reverse=True))      #Lovely, gives us a dictionary of the other courses and the amount of
                                                                                                    #people enrolled in them that are also in this course
                                                                                                    #The dictionary is sorted based on highest to lowest
        self.index = index                #Just an index to keep track of the course

'''Make student objects'''
student_objects=[]
responses = pd.read_excel("filtered_feedback_form_responses.xlsx")
emails = responses['Email Address']
choices = list(responses['Courses that I plan to take in the upcoming semester'])

for i in range(len(emails)):
    dum_shit = choices[i].split(",")

    

    for j in range(len(dum_shit)):
        dum_shit[j] = dum_shit[j].strip()
        
    if "BIO339/639" in dum_shit:
        dum_shit.remove("BIO339/639")
    if "BIO416/716" in dum_shit:
        dum_shit.remove("BIO416/716")

    temp_object = Student(emails[i],dum_shit)
    student_objects.append(temp_object)

#Courses given
course_have_now=[]
for student in student_objects:
    for c in student.course_list:
        course_have_now.append(c.strip())
no_courses_have_now={}
for thing in course_have_now:
    no_courses_have_now[thing] = no_courses_have_now.get(thing,0)+1

#all courses
index=1
for j in list(set(course_have_now)):
    loves={}
    for student in student_objects:
        if j in student.course_list:
            for i in student.course_list:
                if i!=j:
                    loves[i] = loves.get(i,0)+1
    print(j)
    print(index)
    index=index+1
    pprint.pprint(loves)
    print()
    print()
