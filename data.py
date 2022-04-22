"""
Code to append data to the database
"""

import csv
from storage import Student, Class, Subject, Club

student_data = []

with open('csv/student.csv', 'r') as f: # convert student data into a list of dict
    dictreader = csv.DictReader(f)
    for ordered_dict in dictreader:
        ordered_dict['id'] = int(ordered_dict['id'])
        ordered_dict['name'] = str(ordered_dict['name'])
        ordered_dict['age'] = ordered_dict['age']
        ordered_dict['year_enrolled'] = ordered_dict['year_enrolled']
        ordered_dict['graduating_year'] = ordered_dict['graduating_year']
        ordered_dict['class'] = ordered_dict['class']
        student_data.append(dict(ordered_dict))

StudentDB = Student() # create student table
for student in student_data:
    StudentDB.insert(student) # insert student records


class_data = []

with open('csv/class.csv', 'r') as f: # convert cca data into a list of dict
    dictreader = csv.DictReader(f)
    for ordered_dict in dictreader:
        ordered_dict['id'] = int(ordered_dict['id'])
        ordered_dict['name'] = int(ordered_dict['name'])
        ordered_dict['level'] = ordered_dict['level']
        class_data.append(dict(ordered_dict))

ClassDB = Class() # create class table
for class_ in class_data:
    ClassDB.insert(class_) # insert class records


subject_data = []

with open('csv/subject.csv', 'r') as f: # convert subject data into a list of dict
    dictreader = csv.DictReader(f)
    for ordered_dict in dictreader:
        ordered_dict['id'] = int(ordered_dict['id'])
        ordered_dict['name'] = ordered_dict['name']
        ordered_dict['level'] = ordered_dict['level']
        subject_data.append(dict(ordered_dict))

SubjectDB = Subject() # create subject table
for subject in subject_data:
    SubjectDB.insert(subject) # insert subject records


club_data = []

# with open('csv/club.csv', 'r') as f: # convert club  data into a list of dict
#     dictreader = csv.DictReader(f)
#     for ordered_dict in dictreader:
#         ordered_dict['id'] = int(ordered_dict['id'])
#         ordered_dict['name'] = ordered_dict['name']
#         club_data.append(dict(ordered_dict))

# ClubDB = Club() # create club table
# for club in club_data:
#     ClubDB.insert(club) # insert club records
