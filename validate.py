"""Validation Functions"""

def id(value):
    """
    Return
    - True if value is more than 1
    - False otherwise
    """
    if value.isdigit():
        return int(value) >= 1
    else:
        return False

    
def name(value):
    """
    Return
    - True if value is of type str and consists of alphabets only
    - False otherwise
    """
    value = value.replace(' ', '')
    return value.isalpha()


def age(value):
    """
    Return
    - True if value between 16 and 20 (inclusive)
    - False otherwise
    """
    if value.isdigit():
        return 16 <= int(value) <= 20
    else:
        return False


def class_name(value):
    """
    Return
    - True if value is between 1000 and 9999 (inclusive)
    - False otherwise
    """
    if value.isdigit():
        return 1000 <= int(value) <= 9999
    else:
        return False


def class_level(value):
    """
    Return
    - True if value is 'JC1' or 'JC2'
    - False otherwise
    """
    return (value in ['JC1', 'JC2'])


def subject_name(value):
    """
    Return
    - True if value is of a valid subject
    - False otherwise
    """
    subjects = ['GP', 'MATH', 'FM', 'COMP', 'PHY',
                'CHEM', 'ECONS', 'BIO', 'GEO', 'HIST',
                'ELIT', 'ART', 'CLTRANS', 'CL', 'ML',
                'TL', 'CLL', 'CLB', 'PW', 'PUNJABI',
                'HINDI', 'BENGALESE', 'JAPANESE']
    
    return value in subjects


def subject_level(value):
    """
    Return
    - True if value is 'H1', 'H2', 'H3'
    - False otherwise
    """
    return value in ['H1', 'H2', 'H3']


def date(value):
    """
    Return
    - True if value follows a certain format YYYY-MM-DD
    - False otherwise
    """
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
    """
    Return
    - True if value is of type str
    - False otherwise
    """
    return isinstance(value, str)


def membership_role(value):
    """
    Return
    - True if value is 'President', 'Vice President', 'Exco', 'Member'
    - False otherwise
    """
    membership_roles = ['President', 'Vice President', 'Exco', 'Member']
    return value in membership_roles


def participation_role(value):
    """
    Return
    - True if value is 'Participant', 'Facilitator', 'Overall In Charge'
    - False otherwise
    """
    participant_roles = ['Participant', 'Facilitator', 'Overall In Charge']
    return value in participant_roles
    

def category(value):
    """
    Return
    - True if value is 'Achievement', 'Enrichment', 'Leadership', 'Service'
    - False otherwise
    """
    categoryList = ['Achievement', 'Enrichment', 'Leadership', 'Service']
    return value in categoryList


def hours(value):
    """
    Return
    - True if value is more than 0
    - False otherwise
    """
    if value.isdigit():
        return int(value) > 0
    else:
        return False
