import sqlite3
import sql

class Collections:
    """
    Encapsulates a collection of records.
    """
    # initialising the data table
    def __init__(self, table_name): 
        pass

    
    def execute(self, command: str, values=None, **kwargs): 
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            if values == None: 
                cur.execute(command) # execute the command only if there are no additional values
            else:
                cur.execute(command, values) # else execute the command with the values

            result = None
            if kwargs.get('fetchone'):
                result = cur.fetchone()
            elif kwargs.get('fetchall'):
                result = cur.fetchall()
            conn.commit()
            # conn.close() is automatically called
        return result


    def update(self, data_updated, data_checked): 
        # update by checking whether the name matches and changing the student name
        query = """UPDATE """ + self.table + """ SET age = ? WHERE name = ?"""
        param = (data_updated, data_checked)
        self.execute(query, param)


    def delete(self, value): # delete the corresponding name, can change to whatever you want lol
        query = """DELETE FROM """ + self.table + """ WHERE name = ?;"""
        param = (value,)
        self.execute(query, param)
            

    def find(self, value): # find the corresponding name, can change to whatever you want lol
        query = """SELECT * FROM """ + self.table + """ WHERE name = ?;"""
        param = (value,)
        name = self.execute(query, param, fetchone=True)
        return name


    def getMaxID(self): 
        query = """SELECT MAX(ID) FROM """  + self.table + ";"
        maxID = self.execute(query, fetchone=True)
        return maxID[0]
        
class Student(Collections):
    """
    Encapsulates a collection of student records.
    Each record has the following columns:
    - Name: str
    - Age: int
    - Year enrolled: int
    - Graduating year: int
    """
    # initialising the data table for students
    def __init__(self):
        self.table = 'Student'
        self.database = 'nyjc_computing.db'
        super().execute(sql.CREATE_STUDENT)

    
    def insert(self, record: dict):
        if not self.find(record['name']):
            self.execute(sql.INSERT_STUDENT, tuple(record.values()))


class Class(Collections):
    """
    Encapsulates a collection of class records.
    Each record has the following columns:
    - Name: str
    - Level: str {JC1, JC2}
    """
    # initialising the data table for class
    def __init__(self):
        self.table = 'Class'
        self.database = 'nyjc_computing.db'
        self.execute(sql.CREATE_CLASS)

    
    def insert(self, record: dict):
        if not self.find(record['name']):
            self.execute(sql.INSERT_CLASS, tuple(record.values()))

        
class Subject(Collections):
    """
    Encapsulates a collection of subject records.
    Each record has the following columns:
    - Name: str {GP, MATH, FM, COMP, PHY, CHEM, ECONS, BIO, GEO, HIST, ELIT, ART, CLTRANS, CL, ML, TL, CLL, CLB, PW, PUNJABI, HINDI, BENGALESE, JAPANESE}
    - Level: str {H1, H2, H3}
    """
    # initialising the data table for subject
    def __init__(self):
        self.table = 'Subject'
        self.database = 'nyjc_computing.db'
        self.execute(sql.CREATE_SUBJECT)

    
    def insert(self, record: dict):
        if not self.find(record['name']):
            self.execute(sql.INSERT_SUBJECT, tuple(record.values()))

        
class Club(Collections):
    """
    Encapsulates a collection of club records.
    Each record has the following columns:
    - Name: str 
    """
    # initialising the data table for club
    def __init__(self):
        self.table = 'Club'
        self.database = 'nyjc_computing.db'
        self.execute(sql.CREATE_CLUB)

    
    def insert(self, record: dict):
        if self.getMaxID() == None: # if there is no items in the table 
            inserted_pos = 1
        else: # if there are items in the table
            inserted_pos = self.getMaxID() + 1
            
        if not self.find(record['name']):
            record_final = {'id': inserted_pos} # new inserted pos
            record_final.update(record) # insert id into front of dict
            self.execute(sql.INSERT_CLUB, tuple(record_final.values()))

    
class Activity(Collections):
    """
    Encapsulates a collection of activity records.
    Each record has the following columns:
    - Start Date: str (ISO8601 date)
    - End Date: str (optional)
    - Description: str
    """
    # initialising the data table for activity
    def __init__(self):
        self.table = 'Activity'
        self.database = 'nyjc_computing.db'
        self.execute(sql.CREATE_ACTIVITY)

    
    def insert(self, record: dict):
        if self.getMaxID() == None: # if there is no items in the table 
            inserted_pos = 1
        else: # if there are items in the table
            inserted_pos = self.getMaxID() + 1
            
        if not self.find(record['name']):
            record_final = {'id': inserted_pos} 
            record_final.update(record) # insert id into front of dict
            self.execute(sql.INSERT_ACTIVITY, tuple(record_final.values()))
