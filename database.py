import sqlite3

def execute(argument):
    with sqlite3.connect('nyjc_computing.db') as conn:
        cur = conn.cursor()
        cur.execute(argument)
        
def insert_student(data):
    with sqlite3.connect('nyjc_computing.db') as conn:
        cur = conn.cursor()
        cur.execute(
        """CREATE TABLE IF NOT EXISTS Student(
            student_id INTEGER,
            name TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            year_enrolled INTEGER NOT NULL,
            graduating_year INTEGER NOT NULL,
            PRIMARY KEY(student_id)
        ); 
        """)
    
        for record in data:
            cur.execute(
                """INSERT INTO Student VALUES(?, ?, ?, ?, ?), tuple(record.values())
                """)
    
        conn.commit()
        # conn.close() is automatically called


def insert_class(data):
    with sqlite3.connect('nyjc_computing.db') as conn:
        cur = conn.cursor()
        cur.execute(
        """CREATE TABLE IF NOT EXISTS Class(
            class_id INTEGER,
            name TEXT NOT NULL UNIQUE,
            level TEXT NOT NULL,
            PRIMARY KEY(class_id)
        ); 
        """)
    
        for record in data:
            cur.execute(
                """INSERT INTO Class VALUES(?, ?, ?), tuple(record.values())
                """)
    
        conn.commit()
        # conn.close() is automatically called

        
def insert_subject(data):
    with sqlite3.connect('nyjc_computing.db') as conn:
        cur = conn.cursor()
        cur.execute(
        """CREATE TABLE IF NOT EXISTS Subject(
            subject_id INTEGER,
            name TEXT NOT NULL UNIQUE,
            level TEXT NOT NULL,
            PRIMARY KEY(subject_id)
        ); 
        """)
    
        for record in data:
            cur.execute(
                """INSERT INTO Subject VALUES(?, ?, ?), tuple(record.values())
                """)
    
        conn.commit()
        # conn.close() is automatically called


def insert_club(data):
    with sqlite3.connect('nyjc_computing.db') as conn:
        cur = conn.cursor()
        cur.execute(
        """CREATE TABLE IF NOT EXISTS Club(
            club_id INTEGER,
            name TEXT NOT NULL UNIQUE,
            PRIMARY KEY(club_id)
        ); 
        """)
    
        for record in data:
            cur.execute(
                """INSERT INTO Club VALUES(?, ?, ?), tuple(record.values())
                """)
    
        conn.commit()
        # conn.close() is automatically called


def insert_activity(data):
    with sqlite3.connect('nyjc_computing.db') as conn:
        cur = conn.cursor()
        cur.execute(
        """CREATE TABLE IF NOT EXISTS Activity(
            activity_id INTEGER,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            description TEXT,
            PRIMARY KEY(subject_id)
        ); 
        """)
    
        for record in data:
            cur.execute(
                """INSERT INTO Activity VALUES(?, ?, ?), tuple(record.values())
                """)
    
        conn.commit()
        # conn.close() is automatically called