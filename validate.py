"""Validation Functions"""

def id(value):
    if value.isdigit():
        return int(value) >= 1
    else:
        return False

    
def name(value):
    value = value.replace(' ', '')
    return value.isalpha()


def age(value):
    if value.isdigit():
        return 16 <= int(value) <= 20
    else:
        return False


def class_name(value):
    if value.isdigit():
        return 1000 <= int(value) <= 9999
    else:
        return False


def class_level(value):
    return (value in ['JC1', 'JC2'])


def subject_name(value):
    subjects = ['GP', 'MATH', 'FM', 'COMP', 'PHY',
                'CHEM', 'ECONS', 'BIO', 'GEO', 'HIST',
                'ELIT', 'ART', 'CLTRANS', 'CL', 'ML',
                'TL', 'CLL', 'CLB', 'PW', 'PUNJABI',
                'HINDI', 'BENGALESE', 'JAPANESE']
    
    return value in subjects


def subject_level(value):
    return value in ['H1', 'H2', 'H3']


def date(value):
    if len(value) != 10:
        return False

    if not (value[4] == '-' and value[7] == '-'):
        return False

    year, month, day = value.split('-')

    if year.isdigit() and month.isdigit() and day.isdigit():
        return ((2000 <= int(year) <= 2100) and
                (1 <= int(month) <= 12) and
                (1 <= int(day) <= 31))

    else:
        return False


def description(value):
    return isinstance(value, str)


def category(value):
    categoryList = ['Achievement', 'Enrichment', 'Leadership', 'Service']
    return value in categoryList


def hours(value):
    if value.isdigit():
        return int(value) > 0
    else:
        return False
