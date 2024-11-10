import numpy as np
import pprint
import pandas as pd

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
choices = responses['Courses that I plan to take in the upcoming semester']

for i in range(len(emails)):
    dum_shit = choices[i].split(",")
    for j in range(len(dum_shit)):
        dum_shit[j] = dum_shit[j].strip()
    temp_object = Student(emails[i],dum_shit)
    student_objects.append(temp_object)

'''Make course objects'''
fhand = open("Course_interrelationships.txt")

c_list = []
string=[]
for line in fhand:
    if line.strip()!="":
        string.append(line.strip())
    elif line.strip()=="":
        c_list.append(string)
        string=[]

c_list = [q for q in c_list if q != []]

#pprint.pprint(c_list)

ob_list = []
for d in c_list:
    useful = {}
    for i in range(len(d)):
        if i==0 or i==1:
            continue
        else:
            useful[d[i][0:d[i].index(":")]] = int(d[i][d[i].index(":")+1:])
    temp_ob = Course(d[0].strip(),int(d[1]),useful)
    
    ob_list.append(temp_ob)



'''other useful crap'''
course_index = {}
for i in ob_list:
    course_index[i.name] = i.index
#pprint.pprint(course_index)

''' Setting 2019 and 2020 emails '''
emails_2020 = ['abhinyap@students.iisertirupati.ac.in', 'abhiruchisah@students.iisertirupati.ac.in', 'abhisheks@students.iisertirupati.ac.in', 'adhinav@students.iisertirupati.ac.in', 'adithyasuresh@students.iisertirupati.ac.in', 'adityapanigrahy@students.iisertirupati.ac.in', 'afrahmohamed@students.iisertirupati.ac.in', 'aiswaryasukumaran@students.iisertirupati.ac.in', 'aiswaryavijay@students.iisertirupati.ac.in', 'ajaybenny@students.iisertirupati.ac.in', 'akhilaashraf@students.iisertirupati.ac.in', 'althafsaneen@students.iisertirupati.ac.in', 'amalfathima@students.iisertirupati.ac.in', 'amansparsh@students.iisertirupati.ac.in', 'ananyaraj@students.iisertirupati.ac.in', 'anishmukhopadhyay@students.iisertirupati.ac.in', 'anjalikrishna@students.iisertirupati.ac.in', 'anmolbhagat@students.iisertirupati.ac.in', 'annalbaisil@students.iisertirupati.ac.in', 'anugraharajan@students.iisertirupati.ac.in', 'anukrishnap@students.iisertirupati.ac.in', 'anzeerabeegumtm@students.iisertirupati.ac.in', 'aparnac@students.iisertirupati.ac.in', 'aparnad@students.iisertirupati.ac.in', 'arapanroymondal@students.iisertirupati.ac.in', 'arijitpatra@students.iisertirupati.ac.in', 'arindamsamanta@students.iisertirupati.ac.in', 'arjitshankar@students.iisertirupati.ac.in', 'arshjotsingh@students.iisertirupati.ac.in', 'mahangareashish@students.iisertirupati.ac.in', 'asmashirin@students.iisertirupati.ac.in', 'aswinanto@students.iisertirupati.ac.in', 'atharvavijaykumar@students.iisertirupati.ac.in', 'athmikaprajesh@students.iisertirupati.ac.in', 'ayushmanmallick@students.iisertirupati.ac.in', 'balagopal@students.iisertirupati.ac.in', 'bhavyasubi@students.iisertirupati.ac.in', 'chowhanarjun@students.iisertirupati.ac.in', 'dsoujanya@students.iisertirupati.ac.in', 'damodharmanali@students.iisertirupati.ac.in', 'darshandamodaran@students.iisertirupati.ac.in', 'dasarirevathi@students.iisertirupati.ac.in', 'sriharisayee@students.iisertirupati.ac.in', 'derlindavis@students.iisertirupati.ac.in', 'dharanic@students.iisertirupati.ac.in', 'dharanipulukuri@students.iisertirupati.ac.in', 'diyaraj@students.iisertirupati.ac.in', 'diyanamuhammed@students.iisertirupati.ac.in', 'durgar@students.iisertirupati.ac.in', 'farsanaa@students.iisertirupati.ac.in', 'gabbireddy@students.iisertirupati.ac.in', 'gauravsalwan@students.iisertirupati.ac.in', 'godhooly@students.iisertirupati.ac.in', 'gunjankarnwal@students.iisertirupati.ac.in', 'gunjansaroha@students.iisertirupati.ac.in', 'harinisuresh@students.iisertirupati.ac.in', 'hemanthsaigollapudi@students.iisertirupati.ac.in', 'himanisathvika@students.iisertirupati.ac.in', 'husnah@students.iisertirupati.ac.in', 'it@students.iisertirupati.ac.in', 'jasnathasneem@students.iisertirupati.ac.in', 'jhaganr@students.iisertirupati.ac.in', 'kalyanib@students.iisertirupati.ac.in', 'kanaseanuja@students.iisertirupati.ac.in', 'karanchandrakant@students.iisertirupati.ac.in', 'kavyae@students.iisertirupati.ac.in', 'keerthiaiswarya@students.iisertirupati.ac.in', 'krishnapriya@students.iisertirupati.ac.in', 'kutadiusha@students.iisertirupati.ac.in', 'lakshanabalaji@students.iisertirupati.ac.in', 'lakshmit@students.iisertirupati.ac.in', 'vukkemlokeshsubrahmanyam@students.iisertirupati.ac.in', 'maddelanavyasri@students.iisertirupati.ac.in', 'madhumithakrishnaswamy@students.iisertirupati.ac.in', 'madhurnildas@students.iisertirupati.ac.in', 'madhusmitamahanta@students.iisertirupati.ac.in', 'malavikam@students.iisertirupati.ac.in', 'manasans@students.iisertirupati.ac.in', 'manasauppala@students.iisertirupati.ac.in', 'mariyajames@students.iisertirupati.ac.in', 'meenakshiv@students.iisertirupati.ac.in', 'banavathmeghanadhnaik@students.iisertirupati.ac.in', 'mittakadapa@students.iisertirupati.ac.in', 'mudavathpravallika@students.iisertirupati.ac.in', 'mufithamajeed@students.iisertirupati.ac.in', 'mukeshkumar@students.iisertirupati.ac.in', 'namithaj.p@students.iisertirupati.ac.in', 'namithak@students.iisertirupati.ac.in', 'nandakrishna@students.iisertirupati.ac.in', 'nayantharaj@students.iisertirupati.ac.in', 'neeraj@students.iisertirupati.ac.in', 'nehaadarsh@students.iisertirupati.ac.in', 'niharikaashutosh@students.iisertirupati.ac.in', 'pasupuletinehakiran@students.iisertirupati.ac.in', 'pattaaishwarya@students.iisertirupati.ac.in', 'pranavmg@students.iisertirupati.ac.in', 'pranavs@students.iisertirupati.ac.in', 'kambleprashant@students.iisertirupati.ac.in', 'pratikveeresh@students.iisertirupati.ac.in', 'pratikchoudhuri@students.iisertirupati.ac.in', 'preranapravinbarge@students.iisertirupati.ac.in', 'priyanshuraj@students.iisertirupati.ac.in', 'pulijagruthi@students.iisertirupati.ac.in', 'rajagopalp@students.iisertirupati.ac.in', 'rajnishshreeraj@students.iisertirupati.ac.in', 'munjuluriramalakshmi@students.iisertirupati.ac.in', 'rangarirohini@students.iisertirupati.ac.in', 'rcvishnuprasanth@students.iisertirupati.ac.in', 'rifanak@students.iisertirupati.ac.in', 'rishichaurasia@students.iisertirupati.ac.in', 'roshananil@students.iisertirupati.ac.in', 'rushdha@students.iisertirupati.ac.in', 'ssaivenkat@students.iisertirupati.ac.in', 'sdevika@students.iisertirupati.ac.in', 'srrajalekshmi@students.iisertirupati.ac.in', 'saadahmad@students.iisertirupati.ac.in', 'sabdhayinikb@students.iisertirupati.ac.in', 'kalangirsaipraneeth@students.iisertirupati.ac.in', 'sakshigupta@students.iisertirupati.ac.in', 'sanskritisaxena@students.iisertirupati.ac.in', 'smandal@students.iisertirupati.ac.in', 'sayantanmandal@students.iisertirupati.ac.in', 'sejalkhanna@students.iisertirupati.ac.in', 'selvabharathik@students.iisertirupati.ac.in', 'senthilvela@students.iisertirupati.ac.in', 'shalinikumari@students.iisertirupati.ac.in', 'dudekulashekshavali@students.iisertirupati.ac.in','sheminas@students.iisertirupati.ac.in', 'shifanac@students.iisertirupati.ac.in', 'shivangibatish@students.iisertirupati.ac.in', 'shivaniramakrishnan@students.iisertirupati.ac.in', 'shreelekshmir@students.iisertirupati.ac.in', 'pshreyathaa@students.iisertirupati.ac.in', 'snehal@students.iisertirupati.ac.in', 'snehapoludasu@students.iisertirupati.ac.in', 'snehasishnayak@students.iisertirupati.ac.in', 'somdattaroy@students.iisertirupati.ac.in', 'soumikroy@students.iisertirupati.ac.in', 'dharavathsrivani@students.iisertirupati.ac.in', 'subhadipdutta@students.iisertirupati.ac.in', 'sukumarb@students.iisertirupati.ac.in', 'sumedhakesavan@students.iisertirupati.ac.in', 'swaradadeshpande@students.iisertirupati.ac.in', 'swarnirddhadan@students.iisertirupati.ac.in', 'swathikrishnam@students.iisertirupati.ac.in', 'swetapadmasana@students.iisertirupati.ac.in', 'swethap@students.iisertirupati.ac.in', 'tejaswinivenkatramanan@students.iisertirupati.ac.in', 'tikamsavita@students.iisertirupati.ac.in', 'umabharathimesalla@students.iisertirupati.ac.in', 'vaishnavy@students.iisertirupati.ac.in', 'venkatashashank@students.iisertirupati.ac.in', 'vigneshn@students.iisertirupati.ac.in', 'rvigneswaran@students.iisertirupati.ac.in', 'vikramravindra@students.iisertirupati.ac.in', 'virajagiriraj@students.iisertirupati.ac.in', 'vishnuramadas@students.iisertirupati.ac.in', 'vishnupriyak@students.iisertirupati.ac.in', 'vykuntapallavi@students.iisertirupati.ac.in', 'vyshnaratheesh@students.iisertirupati.ac.in', 'yuvansrikanthe@students.iisertirupati.ac.in']

'''Getting total amount of people in each course'''
course_totals={}
for student in student_objects:
    for course in student.course_list:
        course_totals[course] = course_totals.get(course,0)+1
course_totals =  dict(sorted(course_totals.items(), key = lambda item: item[1],reverse=True))  #Orders them from most to least

print()
print()
print()
print()

'''Actual algorithm, First we set up blank group'''
group = {'Group 1': [],
 'Group 2': [],
 'Group 3': [],
 'Group 4': [],
 'Group 5': [],
 'Group 6': [],
 'Group 7': [],
 'Group 8': [],
 'Group 9': [],
 'Group 10': [],
 'Group 11': []}

course_not_to_consider = ['BIO436/736 Experimental Biology Lab I 4', 'PHY415 Advanced Physics Lab III 4','CHM335 Advanced Chem Lab - I 3', 'PHY345 Advanced Physics Lab II 3']
#IIT_Courses = ['MTH333 Indian Mathematics and Astronomy 2', 'MTH416 Probability Theory 4']

for i in course_totals.keys():     #Starts the loop for the courses
    if i in course_not_to_consider:
        continue
    '''Loads the first course as well as its corresponding object'''
    temp_course_name = i
    temp_course_object = ob_list[course_index[temp_course_name]-1]

    '''Loads first course in the grouping so we have something'''
    if list(group.values()) == [[],[],[],[],[],[],[],[],[],[]]:
        group["Group 1"].append(temp_course_name)
        group["Group 2"].append(list(temp_course_object.lovely.keys())[0])
    else:
        #Check if Course already in the group
        course_already_accounted_for = False
        for j in group.values():
            if temp_course_name in j:
                course_already_accounted_for = True
                break
        if course_already_accounted_for == True:
            continue

        '''Add to each successive group and check how many conflicts'''
        no_of_conflicts = None
        group_to_add = None
        #print("================================================================")
        for gr in group.keys():
            test = group[gr].copy()  #Forms a copy of the group to test its conflicts
            test.append(temp_course_name)

            #IIT clash
            #if len(set(test).intersection(set(IIT_Courses))) > 1:
            #    continue

            #checks for professor clash
            #if ('ECS321 - Introduction to Earth and Climate Science' in test) and ('ECS422 - Atmospheric Dynamics' in test):
             #   continue
            #if ('PHY326 - Nonlinear Dynamics' in test) and ('BIO462/CHM462/CSA462/ECS462/PHY462 - Data Science II' in test):
            #    continue
            #if ('BIO462/CHM462/CSA462/ECS462/PHY462 - Data Science II' in test) and ('CHM465 - Supramolecular Architectures to Molecular Machines' in test):
            #    continue
            #if ('CHM323 - Organometallic Chemistry' in test) and ('CHM423 - Chemistry of d- and f- Block Elements' in test):
            #    continue
            #if ('MTH441 - Operations Research' in test) and ('PHY442 - Plasma Physics' in test):
            #    continue

            #if ('PHY324 - Solid State Physics' in test) and ('MTH323 - Analysis in Euclidean Spaces' in test):
            #    continue
            #if ('PHY442 - Plasma Physics' in test) and ('CHM464 - Astrochemistry' in test):
            #    continue
            #if ('CHM422 - Organic Synthesis II' in test) and ('CHM464 - Astrochemistry' in test):
            #    continue

            #if len(test) == 6:   #this line gives indirectly the maximum amount of course in a group
                #continue
            
            conflicts = 0
            '''Find no. of conflicts if this course were added in this group'''
            for student in student_objects:
                if student.checkIfWorksOneGroup(test) == False:
                    conflicts = conflicts+1
                else:
                    continue
            #print((no_of_conflicts == None) or (conflicts <= no_of_conflicts))
            '''Pick out the group with the minimum amount of conflicts'''
            if (no_of_conflicts == None) or (conflicts <= no_of_conflicts) :
                no_of_conflicts = conflicts
                group_to_add = gr   
        
        #print(type(group_to_add))
        '''Actually add the course to the group'''
        group[group_to_add].append(temp_course_name)

pprint.pprint(group)  #Run this again to see original grouping
print()
print()

'''Calculating the amount of people who would be ok with the schedule'''
result = []
for student in student_objects:
    result.append(student.checkIfWorks(group))

metric = 0
for i in result:
    if i==True:
        metric=metric+1

print("The total amount of students who gave input are "+str(len(student_objects)))
print("The total amount of people agreeing with this grouping is " + str(metric))

#Seeing which students have clashes
clashed_groups={}
for student in student_objects:
    if student.groupClash == True:
        print(student.email)
        print(student.whyGroupClash)
        print(student.whichGroupClash)
        print()
        for c in student.whyGroupClash:
            clashed_groups[c] = clashed_groups.get(c,0)+1

''' counting amount of course in grouping '''
tot = 0
for g in group.keys():
    tot = tot + len(group[g])
print("The total amount of coruses in the grouping is "+ str(tot))
