import sqlite3
import sql

class Collections:
    """
    Encapsulates a collection of records.
    """
    # initialising the data table
    def __init__(self, table_name): # table = sql.CREATE_ (respective table)
        self.table = table_name

    def execute(self, command: str, values=None):
        with sqlite3.connect('nyjc_computing.db') as conn:
            cur = conn.cursor()
            if values == None:
                cur.execute(command)
            else:
                cur.execute(command, values)
                
            conn.commit()
            # conn.close() is automatically called

    def insert(self, command: str, record: dict):
        # breakpoint()
        self.execute(command, tuple(record.values()))
        

    def update(self, col, data_updated, data_checked): # idk whether it works lmao
        with sqlite3.connect('nyjc_computing.db') as conn:
            cur = conn.cursor()
            cur.execute(f"""
        UPDATE {self.table}
        SET ? = ?
        WHERE id = ?;
                """,
                (col, data_updated, data_checked),
            )
            conn.commit()


    def delete(self, key, value):
        with sqlite3.connect('nyjc_computing.db') as conn: # idk whether it works lmao
            cur = conn.cursor()
            cur.execute(f"""
        DELETE FROM {self.table}
        WHERE ? = ?;
                """,
                (key, value),
            )
            conn.commit()
        return

    def find(self, key, value):
        with sqlite3.connect('nyjc_computing.db') as conn: # idk whether it works lmao
            cur = conn.cursor()
            cur.execute(f"""
        SELECT *
        FROM {self.table}
        WHERE ? = ?; 
            """, 
            (key, value)
        )
            record = cur.fetchone()
            
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
        # with sqlite3.connect(db_uri) as conn:
        #     cur = conn.cursor()
        #     cur.execute(sql.CREATE_STUDENT)
        #     conn.commit()
        # conn.close() is automatically called

        self.execute(sql.CREATE_STUDENT)


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
        # with sqlite3.connect(db_uri) as conn:
        #     cur = conn.cursor()
        #     cur.execute(sql.CREATE_CLASS)
        #     conn.commit()
        # conn.close() is automatically called

        self.execute(sql.CREATE_CLASS)

        
class Subject(Collections):
    """
    Encapsulates a collection of subject records.
    Each record has the following columns:
    - Name: str {GP, MATH, FM, COMP, PHY, CHEM, ECONS, BIO, GEO, HIST, ELIT, ART, CLTRANS, CL, ML, TL, CLL, CLB, PW, PUNJABI, HINDI, BENGALESE, JAPANESE}
    - Level: str {H1, H2, H3}
    """
    # initialising the data table for class
    def __init__(self):
        self.table = 'Subject'
        # with sqlite3.connect(db_uri) as conn:
        #     cur = conn.cursor()
        #     cur.execute(sql.CREATE_SUBJECT)
        #     conn.commit()
        # conn.close() is automatically called

        self.execute(sql.CREATE_SUBJECT)

    
class Club(Collections):
    """
    Encapsulates a collection of club records.
    Each record has the following columns:
    - Name: str 
    """
    # initialising the data table for class
    def __init__(self):
        self.table = 'Club'
        # with sqlite3.connect(db_uri) as conn:
        #     cur = conn.cursor()
        #     cur.execute(sql.CREATE_CLUB)
        #     conn.commit()
        # conn.close() is automatically called

        self.execute(sql.CREATE_CLUB)

    
class Activity(Collections):
    """
    Encapsulates a collection of student records.
    Each record has the following columns:
    - Start Date: str (ISO8601 date)
    - End Date: str (optional)
    - Description: str
    """
    # initialising the data table for class
    def __init__(self):
        self.table = 'Activity'
        # with sqlite3.connect(db_uri) as conn:
        #     cur = conn.cursor()
        #     cur.execute(sql.CREATE_ACTIVITY)
        #     conn.commit()
        # conn.close() is automatically called

        self.execute(sql.CREATE_ACTIVITY)
    