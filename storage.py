import sqlite3
import sql

class Collections:
    """
    Encapsulates a collection of records.
    """
    # initialising the data table
    def __init__(self):
        pass

    def execute(self, command, values=None):
        with sqlite3.connect('nyjc_computing.db') as conn:
            cur = conn.cursor()
            if values == None:
                cur.execute(command)
            else:
                cur.execute(command, values)
        conn.commit()
        # conn.close() is automatically called

    def insert(self, table, data):
#         with sqlite3.connect('nyjc_computing.db') as conn:
#             cur = conn.cursor()
#             cur.execute("""
# INSERT into Student VALUES (?, ?, ?)""", 
# tuple(data.values()))
        pass

    def update(self, table, col_checked, col_updated, data_checked, data_updated): # idk whether it works lmao
        with sqlite3.connect('nyjc_computing.db') as conn:
            cur = conn.cursor()
            cur.execute(f"""
        UPDATE {table}
        SET {col_updated} = ?
        WHERE {col_checked} = ?;
                """,
                (data_updated, data_checked),
            )
            conn.commit()

        pass

    def delete(self, table, col, data):
        with sqlite3.connect('nyjc_computing.db') as conn: # idk whether it works lmao
            cur = conn.cursor()
            cur.execute(f"""
        DELETE FROM {table}
        WHERE {col} = ?;
                """,
                (data,),
            )
            conn.commit()


        pass

    def find(self, cols, table):
        pass
        
        
class Student(Collections):
    """
    Encapsulates a collection of student records.
    Each record has the following columns:
    - Name: str
    - Age: int
    - Year enrolled: int
    - Graduating year: int
    """
    table = 'Student'
    # initialising the data table for students
    def __init__(self, db_uri = 'nyjc_computing.db'):
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
    table = 'Class'
    # initialising the data table for class
    def __init__(self, db_uri = 'nyjc_computing.db'):
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
    table = 'Subject'
    # initialising the data table for class
    def __init__(self, db_uri = 'nyjc_computing.db'):
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
    table = 'Club'
    # initialising the data table for class
    def __init__(self, db_uri = 'nyjc_computing.db'):
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
    table = 'Activity'
    # initialising the data table for class
    def __init__(self, db_uri = 'nyjc_computing.db'):
        # with sqlite3.connect(db_uri) as conn:
        #     cur = conn.cursor()
        #     cur.execute(sql.CREATE_ACTIVITY)
        #     conn.commit()
        # conn.close() is automatically called

        self.execute(sql.CREATE_ACTIVITY)
    