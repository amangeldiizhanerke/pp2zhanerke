# super() allows the child class to inherit all methods and properties
# from the parent class

class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)  # calls Person's __init__

x = Student("John", "Doe")

print(x.firstname)  # Output: John
print(x.lastname)   # Output: Doe
