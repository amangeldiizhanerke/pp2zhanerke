class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

class Student:
  def __init__(self, school):
    self.school = school

class Graduate(Person, Student):
  def __init__(self, fname, lname, school):
    Person.__init__(self, fname, lname)
    Student.__init__(self, school)

x = Graduate("John", "Doe", "MIT")

print(x.firstname)  # Output: John
print(x.school)     # Output: MIT
