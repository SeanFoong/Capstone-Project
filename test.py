# testing code
# student records
student1 = {'id': 1, 'student_name': 'bob', 'age': 21, 'year_enrolled': 2021, 'graduating_year': 2023, 'class': '2201'}
student2 = {'id': 2, 'student_name': 'tom', 'age': 18, 'year_enrolled': 2020, 'graduating_year': 2022, 'class': '2101'}
student3 = {'id': 3, 'student_name': 'john', 'age': 16, 'year_enrolled': 2021, 'graduating_year': 2023, 'class': '2101'}

# class records
class1 = {'id': 1, 'class_name': '2201', 'level': 'JC1'}
class2 = {'id': 2, 'class_name': '2101', 'level': 'JC2'}

# student obj + inserting to database
Students = Student()
Students.insert(student1)
Students.insert(student2)
Students.insert(student3)

# class obj + inserting to database
Classes = Class()
Classes.insert(class1)
Classes.insert(class2)

Students.find(4)
Students.find(2)
Students.find(3)
print()

Students.delete(4)
Students.update('jane', 2)
Students.find(1)
Students.find(2)
Students.find(3)