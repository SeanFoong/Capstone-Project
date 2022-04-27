"""SQL Commands"""

# functions for creating the tables in sql

CREATE_STUDENT = """
CREATE TABLE IF NOT EXISTS Student(
    id INTEGER,
    name TEXT,
    age INTEGER,
    year_enrolled INTEGER,
    graduating_year INTEGER,
    class INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY(class) REFERENCES Class(id)
); """


CREATE_CLASS = """
CREATE TABLE IF NOT EXISTS Class(
    id INTEGER,
    name INTEGER,
    level TEXT CHECK (level in ('JC1', 'JC2')),
    PRIMARY KEY(id)
); """


CREATE_SUBJECT = """
CREATE TABLE IF NOT EXISTS Subject(
    id INTEGER,
    name TEXT CHECK (name in 
                ('GP', 'MATH', 'FM', 'COMP', 'PHY', 'CHEM',
                 'ECONS', 'BIO', 'GEO', 'HIST', 'ELIT', 'ART',
                 'CLTRANS', 'CL', 'ML', 'TL', 'CLL', 'CLB',
                 'PW', 'PUNJABI', 'HINDI', 'BENGALESE', 'JAPANESE')),
    level TEXT CHECK (level in ('H1', 'H2', 'H3')),
    PRIMARY KEY(id)
); """


CREATE_CLUB = """
CREATE TABLE IF NOT EXISTS Club(
    id INTEGER,
    name TEXT,
    PRIMARY KEY(id)
); """


CREATE_ACTIVITY = """
CREATE TABLE IF NOT EXISTS Activity(
    id INTEGER,
    name TEXT,
    start_date TEXT,
    end_date TEXT,
    description TEXT,
    PRIMARY KEY(id)
); """


CREATE_STUDENT_SUBJECT = """
CREATE TABLE IF NOT EXISTS Student_Subject(
    student_id INTEGER,
    subject_id INTEGER,
    PRIMARY KEY(student_id, subject_id),
    FOREIGN KEY(student_id) REFERENCES Student(id),
    FOREIGN KEY(subject_id) REFERENCES Subject(id)
); """


CREATE_MEMBERSHIP = """
CREATE TABLE IF NOT EXISTS Membership(
    student_id INTEGER,
    club_id INTEGER,
    role TEXT DEFAULT 'Member',
    PRIMARY KEY(student_id, club_id),
    FOREIGN KEY(student_id) REFERENCES Student(id),
    FOREIGN KEY(club_id) REFERENCES Club(id)
); """


CREATE_PARTICIPATION = """
CREATE TABLE IF NOT EXISTS Participation(
    student_id INTEGER,
    club_id INTEGER,
    activity_id INTEGER,
    category TEXT CHECK (category in ('Achievement', 'Enrichment', 'Leadership', 'Service')),
    role TEXT DEFAULT 'Participant',
    award TEXT,
    hours INTEGER,
    PRIMARY KEY(student_id, club_id, activity_id),
    FOREIGN KEY(student_id) REFERENCES Student(id),
    FOREIGN KEY(club_id) REFERENCES Club(id),
    FOREIGN KEY(activity_id) REFERENCES Activity(id)
); """


# functions parameterised insertion for the different tables

INSERT_STUDENT = """
INSERT INTO Student VALUES (?, ?, ?, ?, ?, ?)
;"""


INSERT_CLASS = """
INSERT INTO Class VALUES (?, ?, ?)
"""


INSERT_SUBJECT = """
INSERT INTO Subject VALUES (?, ?, ?)
"""


INSERT_CLUB = """
INSERT INTO Club VALUES (?, ?)
"""


INSERT_ACTIVITY = """
INSERT INTO Activity VALUES (?, ?, ?, ?, ?)
"""
