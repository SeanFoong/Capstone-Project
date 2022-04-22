import sqlite3
import sql

class Collections:
    """
    Encapsulates a collection of records.
    """
    # initialising the data table
    def __init__(self, table_name): 
        pass

    
    def execute(self, command: str, values=None): 
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            if values == None: 
                cur.execute(command) # execute the command only if there are no additional values
            else:
                cur.execute(command, values) # else execute the command with the values
                
            conn.commit()
            # conn.close() is automatically called


    def update(self, data_updated, data_checked): 
        # update by checking whether the id matches and changing the student name
        with sqlite3.connect(self.database) as conn: # yes it does 
            query = """UPDATE """ + self.table + """ SET student_name = ? WHERE id = ?"""
            param = (data_updated, data_checked)
            cur = conn.cursor()
            cur.execute(query, param)
            conn.commit()


    def delete(self, value): # delete the corresponding id, can change to whatever you want lol
        with sqlite3.connect(self.database) as conn: # it works now
            query = """DELETE FROM """ + self.table + """ WHERE id = ?;"""
            param = (value, )
            cur = conn.cursor()
            cur.execute(query, param)
            conn.commit()
            

    def find(self, value): # find the corresponding id, can change to whatever you want lol
        with sqlite3.connect(self.database) as conn: # note to self, you cannot parameterise the table name aand column, only the values fml
            query = """SELECT * FROM """ + self.table + """ WHERE id = ?;"""
            param = (value,)
            cur = conn.cursor()
            cur.execute(query, param)
            record = cur.fetchone()

        print(record) # can comment this out just testing this on console lmao
        return record
        
        
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
        if not self.find(record['id']):
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
        if not self.find(record['id']):
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
        if not self.find(record['id']):
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
        if not self.find(record['id']):
            self.execute(sql.INSERT_CLUB, tuple(record.values()))

    
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
        # breakpoint()
        if not self.find(record['id']):
            print('yes')
            self.execute(sql.INSERT_ACTIVITY, tuple(record.values()))

