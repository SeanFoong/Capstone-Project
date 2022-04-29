"""
Code to append data to the database
"""

import csv
from storage import Student, Class, Subject, Club, StudentSubject

def import_student():
    with open('csv/student.csv', 'r') as f:
        dictreader = csv.DictReader(f)
        for ordered_dict in dictreader:
            ordered_dict['id'] = int(ordered_dict['id'])
            ordered_dict['name'] = str(ordered_dict['name'])
            ordered_dict['age'] = ordered_dict['age']
            ordered_dict['year_enrolled'] = ordered_dict['year_enrolled']
            ordered_dict['graduating_year'] = ordered_dict['graduating_year']
            ordered_dict['class'] = ordered_dict['class']
            StudentDB.insert(ordered_dict) # insert student records


def import_class():
    with open('csv/class.csv', 'r') as f: # convert cca data into a list of dict
        dictreader = csv.DictReader(f)
        for ordered_dict in dictreader:
            ordered_dict['id'] = int(ordered_dict['id'])
            ordered_dict['name'] = int(ordered_dict['name'])
            ordered_dict['level'] = ordered_dict['level']
            ClassDB.insert(ordered_dict) # insert class records


def import_subject():
    with open('csv/subject.csv', 'r') as f: # convert subject data into a list of dict
        dictreader = csv.DictReader(f)
        for ordered_dict in dictreader:
            ordered_dict['id'] = int(ordered_dict['id'])
            ordered_dict['name'] = ordered_dict['name']
            ordered_dict['level'] = ordered_dict['level']
            SubjectDB.insert(ordered_dict) # insert subject records


def import_club():
    with open('csv/club.csv', 'r') as f: # convert club data into a list of dict
        dictreader = csv.DictReader(f)
        for ordered_dict in dictreader:
            ordered_dict['id'] = int(ordered_dict['id'])
            ordered_dict['name'] = ordered_dict['name']
            ClubDB.insert(ordered_dict) # insert club records


def import_student_subject():
    with open('csv/student_subject.csv', 'r') as f: # convert club data into a list of dict
        dictreader = csv.DictReader(f)
        for ordered_dict in dictreader:
            ordered_dict['student_id'] = int(ordered_dict['student_id'])
            ordered_dict['subject_id'] = ordered_dict['subject_id']
            StudentSubjectDB.insert(ordered_dict) # insert club records

            
# initialisation of the databases
StudentDB = Student()
ClassDB = Class()
SubjectDB = Subject()
ClubDB = Club()
StudentSubjectDB = StudentSubject()

# importing the data from the csvs
import_student()
import_class()
import_subject()
import_club()
import_student_subject()