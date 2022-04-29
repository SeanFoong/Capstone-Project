import sqlite3
import sql

class Collections:
    """
    Encapsulates a collection of records.
    """
    # Initialising the data table
    def __init__(self, table_name): 
        """
        Will be initialised in the child classes
        """
        pass

    
    def execute(self, command: str, values=None, **kwargs): 
        """
        An execute function which gets a cursor object and execute the command from the arguments and returns a result
        """
        with sqlite3.connect(self._database) as conn:
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
        """
        Update by checking whether the name matches and changing the respective name
        """
        query = """UPDATE """ + self._table + """ SET name = ? WHERE name = ?;"""
        param = (data_updated, data_checked)
        self.execute(query, param)


    def delete(self, value): 
        """
        Delete the corresponding data associated to the name
        """
        query = """DELETE FROM """ + self._table + """ WHERE name = ?;"""
        param = (value,)
        self.execute(query, param)
            

    def find(self, value): 
        """
        Find the corresponding data associated to the name
        """
        query = """SELECT * FROM """ + self._table + """ WHERE name = ?;"""
        param = (value,)
        result = self.execute(query, param, fetchone=True)
        
        if result is None: # record is not found
            return result

        # get the column names in the table
        col_query = """SELECT * FROM """ + self._table 
        with sqlite3.connect(self._database) as conn:
            cur = conn.execute(col_query)
            col_names = list(map(lambda x: x[0], cur.description)) 

        index = 0
        record = {} # record[col_names] = result[idx]
        
        # inserting results into the dict
        for col in col_names: 
            record[col] = result[index]
            index += 1
            
        return record # return a dict 


    def findAll(self):
        """
        Find all the names in the respective table
        """
        query = """SELECT name FROM """ + self._table + ";"
        data = self.execute(query, fetchall=True) # returns a list of tuples

        # convert the list of tuples to a list of names
        name_list = []
        
        for name in data:
            name_list.append(name[0])
            
        return name_list

    def findID(self, value):  
        """
        Find the corresponding id associated to the name
        """
        query = """SELECT id FROM """ + self._table + """ WHERE name = ?;"""
        param = (value,)
        id = self.execute(query, param, fetchone=True) # id is a set and first value is the id
        
        if id is None:  # ID does not exist
            return None
        else:
            return id[0]
        

    def getMaxID(self): 
        """
        Find the largest id from the table
        """
        query = """SELECT MAX(ID) FROM """  + self._table + ";"
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
    def __init__(self):
        """
        Initialising the data table for students
        """
        self._table = 'Student'
        self._database = 'nyjc_computing.db'
        super().execute(sql.CREATE_STUDENT)

    
    def insert(self, record: dict):
        if not self.find(record['name']): # checks if student name exist
            self.execute(sql.INSERT_STUDENT, tuple(record.values()))


class Class(Collections):
    """
    Encapsulates a collection of class records.
    Each record has the following columns:
    - Name: str
    - Level: str {JC1, JC2}
    """
    def __init__(self):
        """
        Initialising the data table for class
        """
        self._table = 'Class'
        self._database = 'nyjc_computing.db'
        self.execute(sql.CREATE_CLASS)

    
    def insert(self, record: dict):
        """
        Insert class into the Class table
        """
        if not self.find(record['name']): # checks if class name exist
            self.execute(sql.INSERT_CLASS, tuple(record.values()))

        
class Subject(Collections):
    """
    Encapsulates a collection of subject records.
    Each record has the following columns:
    - Name: str {GP, MATH, FM, COMP, PHY, CHEM, ECONS, BIO, GEO, HIST, ELIT, ART, CLTRANS, CL, ML, TL, CLL, CLB, PW, PUNJABI, HINDI, BENGALESE, JAPANESE}
    - Level: str {H1, H2, H3}
    """
    # 
    def __init__(self):
        """
        Initialising the data table for subject
        """
        self._table = 'Subject'
        self._database = 'nyjc_computing.db'
        self.execute(sql.CREATE_SUBJECT)

    
    def insert(self, record: dict):
        """
        Insert subject into the Subject table
        """
        if not self.find(record['name']): # checks if subject name exist
            self.execute(sql.INSERT_SUBJECT, tuple(record.values()))

        
class Club(Collections):
    """
    Encapsulates a collection of club records.
    Each record has the following columns:
    - Name: str 
    """
    def __init__(self):
        """
        Initialising the data table for club
        """
        self._table = 'Club'
        self._database = 'nyjc_computing.db'
        self.execute(sql.CREATE_CLUB)

    
    def insert(self, record: dict):
        """
        Insert club into the Club table
        """
        if self.getMaxID() == None: # if there is no items in the table 
            inserted_pos = 1
        else: # if there are items in the table
            inserted_pos = self.getMaxID() + 1
            
        if not self.find(record['name']): # checks if club name exist
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
    def __init__(self):
        """
        Initialising the data table for activity
        """
        self._table = 'Activity'
        self._database = 'nyjc_computing.db'
        self.execute(sql.CREATE_ACTIVITY)

    
    def insert(self, record: dict):
        """
        Insert activity into the Activity table
        """
        if self.getMaxID() == None: # if there is no items in the table 
            inserted_pos = 1
        else: # if there are items in the table
            inserted_pos = self.getMaxID() + 1
            
        if not self.find(record['name']):
            record_final = {'id': inserted_pos} 
            record_final.update(record) # insert id into front of dict
            self.execute(sql.INSERT_ACTIVITY, tuple(record_final.values()))


class StudentSubject(Collections):
    """
    Encapsulates a collection of activity records.
    Each record has the following columns:
    - Student_id: int
    - Subject_id: int
    """
    def __init__(self):
        """
        Initialising the data table for StudentSubject
        """
        self._table = 'Student_Subject'
        self._database = 'nyjc_computing.db'
        self.execute(sql.CREATE_STUDENT_SUBJECT)


    def insert(self, record: dict):
        """
        Insert student_subject into the StudentSubject table
        """
        student_id = record['student_id']
        subject_id = record['subject_id']
        if not self.find(student_id, subject_id):
            self.execute(sql.INSERT_STUDENT_SUBJECT, tuple(record.values()))

            
    def find(self, student_id, subject_id): 
        """
        Find the corresponding data with the student_id and subject_id provided
        """
        query = """SELECT * FROM """ + self._table + \
                """ WHERE student_id = ? and subject_id = ?;"""
        param = (student_id, subject_id)
        result = self.execute(query, param, fetchone=True)

        if result is None: # record is not found
            return result

        col_query = """SELECT * FROM """ + self._table # get col names in table
        conn = sqlite3.connect(self._database)
        cursor = conn.execute(col_query)
        col_names = list(map(lambda x: x[0], cursor.description)) 

        record = {} # insert record[col_names] = result into dict
        index = 0
        for col in col_names:
            record[col] = result[index]
            index += 1

        return record # return a dict
        

class Membership(Collections):
    def __init__(self):
        """
        Initialising the data table for Membership
        """
        self._table = 'Membership'
        self._database = 'nyjc_computing.db'
        self.execute(sql.CREATE_MEMBERSHIP)


    def insert(self, record: dict):
        """
        Insert Membership into the Membership table"""
        self.execute(sql.INSERT_MEMBERSHIP, tuple(record.values()))
            
    
    def find(self, student_id, club_id): 
        """
        Find the corresponding data with the student name provided
        """
        query = """SELECT * FROM """ + self._table + \
                """ WHERE student_id = ? and club_id = ?;"""
        param = (student_id, club_id)
        result = self.execute(query, param, fetchone=True)

        if result is None: # record is not found
            return result

        col_query = """SELECT * FROM """ + self._table # get col names in table
        conn = sqlite3.connect(self._database)
        cursor = conn.execute(col_query)
        col_names = list(map(lambda x: x[0], cursor.description)) 

        record = {} # insert record[col_names] = result into dict
        index = 0
        for col in col_names:
            record[col] = result[index]
            index += 1
            
        return record # return a dict 


    def update(self, role, student_id, club_id): 
        """
        Update by checking whether the club and the role for one student
        """
        query = """UPDATE """ + self._table + \
                """ SET role = ? 
                WHERE student_id = ? and club_id = ?"""
        param = (role, student_id, club_id)
        self.execute(query, param)


class Participation(Collections):
    def __init__(self):
        """
        Initialising the data table for Participation
        """
        self._table = 'Participation'
        self._database = 'nyjc_computing.db'
        self.execute(sql.CREATE_PARTICIPATION)


    def insert(self, record: dict):
        """
        Insert participation into the Participation table
        """
        self.execute(sql.INSERT_PARTICIPATION, tuple(record.values()))
        
        
    def find(self, student_id, club_id, activity_id):  
        """
        Find the corresponding data with the student name provided
        """
        query = """SELECT * FROM """ + self._table + \
                """ WHERE student_id = ? and club_id = ? and activity_id = ?;"""
        param = (student_id, club_id, activity_id)
        result = self.execute(query, param, fetchone=True)
        
        if result is None: # record is not found
            return result

        col_query = """SELECT * FROM """ + self._table # get col names in table
        conn = sqlite3.connect(self._database)
        cursor = conn.execute(col_query)
        col_names = list(map(lambda x: x[0], cursor.description)) 

        record = {} # insert record[col_names] = result into dict
        index = 0
        for col in col_names:
            record[col] = result[index]
            index += 1
            
        return record # return a dict 

    
    def update(self, category, role, award, hours, student_id, club_id, activity_id): 
        """
        Update by checking whether the activity and the role for one student
        """
        query = """UPDATE """ + self._table + \
                """ SET category = ?, role = ?, award = ?, hours = ? 
                WHERE student_id = ? and club_id = ? and activity_id = ?"""
        param = (category, role, award, hours, student_id, club_id, activity_id)
        self.execute(query, param)