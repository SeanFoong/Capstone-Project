def name(value):
    if isinstance(value, str):
        return value.istitle()
    else:
        return False


def class_name(value):
    if isinstance(value, int):
        return 1000 <= value <= 9999
    else:
        return False


def class_level(value):
    return (value in ['J1', 'J2'])


def age(value):
    if isinstance(value, int):
        return 16 <= value
    else:
        return False


def date(value):
    if isinstance(value, str):
        return len(value) == 10
    else:
        return False


def category(value):
    return value in ['Achievement',
                     'Enrichment',
                     'Leadership',
                     'Service']


def subject_name(value):
    subjects = ['GP', 'MATH', 'FM', 'COMP', 'PHY',
                'CHEM', 'ECONS', 'BIO', 'GEO', 'HIST',
                'ELIT', 'ART', 'CLTRANS', 'CL', 'ML',
                'TL', 'CLL', 'CLB', 'PW', 'PUNJABI',
                'HINDI', 'BENGALESE', 'JAPANESE']
    
    return value in subjects


def subject_level(value):
    return value in ['H1', 'H2', 'H3']