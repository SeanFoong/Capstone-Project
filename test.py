import sqlite3

def execute(command, values=None):
    with sqlite3.connect('clarencebigdumb.db') as conn:
        cur = conn.cursor()
        if values == None:
            cur.execute(command)
        
        else:
            cur.execute(command, values)
        
        
def insert_student(data):
    execute(
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
        print(record)
        print(record.values())
        execute(
        ("""INSERT INTO Student VALUES(?, ?, ?, ?, ?, ?);
        """, tuple(record.values())))
            
    
    # conn.close() is automatically called
        
import csv
data = []
with open('student.csv', 'r') as f:
    # The DictReader class allows each row of CSV data to be
    # accessed as a dict, with headers automatically detected
    dictreader = csv.DictReader(f)
    for ordered_dict in dictreader:
        ordered_dict['student_id'] = int(ordered_dict['student_id'])
        ordered_dict['year_enrolled'] = int(ordered_dict['year_enrolled'])
        ordered_dict['tshirt_size'] = ordered_dict['tshirt_size']
        data.append(dict(ordered_dict))
# print(data)
insert_student(data)