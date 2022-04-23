import sqlite3
import sql

class Collections:
    """
    Encapsulates a collection of records.
    """
    # Initialising the data table
    def __init__(self, table_name): 
        pass

    
    def execute(self, command: str, values=None, **kwargs): 
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            if values == None: 
                # Execute the command only if there are no additional values
                cur.execute(command) 
            else:
                # Else execute the command with the values
                cur.execute(command, values) 

            result = None
            if kwargs.get('fetchone'):
                result = cur.fetchone()
            elif kwargs.get('fetchall'):
                result = cur.fetchall()
            conn.commit()
            # conn.close() is automatically called
        return result


    def update(self, data_updated, data_checked): 
        # Update by checking whether the name matches and changing the student name
        query = """UPDATE """ + self.table + """ SET name = ? WHERE name = ?"""
        param = (data_updated, data_checked)
        self.execute(query, param)


    def delete(self, value): 
        """Delete the corresponding data associated to the name"""
        query = """DELETE FROM """ + self.table + """ WHERE name = ?;"""
        param = (value,)
        self.execute(query, param)
            

    def find(self, value): 
        """Find the corresponding data associated to the name"""
        query = """SELECT * FROM """ + self.table + """ WHERE name = ?;"""
        param = (value,)
        result = self.execute(query, param, fetchone=True)
        return result


    def findID(self, value):  
        """Find the corresponding id associated to the name"""
        query = """SELECT id FROM """ + self.table + """ WHERE name = ?;"""
        param = (value,)
        id = self.execute(query, param, fetchone=True) # id is a set and first value is the id
        
        if id is None:  # ID does not exist
            return None
        else:
            return id[0]
        

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


class StudentClub(Collections):
    # initialising the data table for student club
    def __init__(self):
        self.table = 'Student_Club'
        self.database = 'nyjc_computing.db'
        self.execute(sql.CREATE_STUDENT_CLUB)

    
    def find(self, student_id, club_id): 
        """Find the corresponding data with the student name provided"""
        query = """SELECT * FROM """ + self.table + """ WHERE student_id = ? and club_id = ?;"""
        param = (student_id, club_id)
        result = self.execute(query, param, fetchone=True)
        return result


    def update(self, club_id, role, student_id): 
        """Update by checking whether the club and the role for one student"""
        query = """UPDATE """ + self.table + """ SET club_id = ?, role = ? WHERE student_id = ?"""
        param = (club_id, role, student_id)
        self.execute(query, param)


class StudentActivity(Collections):
    # initialising the data table for student activity
    def __init__(self):
        self.table = 'Student_Activity'
        self.database = 'nyjc_computing.db'
        self.execute(sql.CREATE_STUDENT_ACTIVITY)

    
    def find(self, student_id, activity_id):  
        """Find the corresponding data with the student name provided"""
        query = """SELECT * FROM """ + self.table + """ WHERE student_id = ? and activity_id = ?;"""
        param = (student_id, activity_id)
        result = self.execute(query, param, fetchone=True)
        return result

    
    def update(self, activity_id, category, role, award, hours, student_id): 
        """Update by checking whether the activity and the role for one student"""
        query = """UPDATE """ + self.table + """ SET activity_id = ?, category = ?, role = ?, award = ?, hours = ? WHERE student_id = ?"""
        param = (activity_id, category, role, award, hours, student_id)
        self.execute(query, param)

