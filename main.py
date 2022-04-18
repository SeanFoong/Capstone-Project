from storage import Collections
from sql import CREATE_STUDENT, INSERT_STUDENT
record = {'id': 1, 'name': 'bob', 'age': 12, 'year_enrolled': 2021, 'graduating_year': 2023, 'class': '4-32'}
# id, :name, :age, :year_enrolled, :graduating_year, :class

Coll = Collections(CREATE_STUDENT)
# Coll.insert(INSERT_STUDENT, (record))
Coll.update(12, 'bob')
Coll.find('bob')

