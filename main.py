from storage import Student, Class
# testing code
# student records
student1 = {'id': 1, 'student_name': 'bob', 'age': 21, 'year_enrolled': 2021, 'graduating_year': 2023, 'class': '4-32'}
student2 = {'id': 2, 'student_name': 'tom', 'age': 18, 'year_enrolled': 2020, 'graduating_year': 2022, 'class': '4-56'}
student3 = {'id': 3, 'student_name': 'john', 'age': 16, 'year_enrolled': 2021, 'graduating_year': 2023, 'class': '4-32'}

# class records
class1 = {'id': 1, 'class_name': '4-32', 'level': 'JC1'}
class2 = {'id': 2, 'class_name': '4-56', 'level': 'JC2'}

# student obj + inserting to database
Students = Student()
Students.insert(student1)
Students.insert(student2)
Students.insert(student3)

# class obj + inserting to database
Class1 = Class()
Class1.insert(class1)
Class1.insert(class2)

Students.find(4)
Students.find(2)
Students.find(3)
print()

Students.delete(4)
Students.update('jane', 2)
Students.find(1)
Students.find(2)
Students.find(3)