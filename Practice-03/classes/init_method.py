#Example 1:
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname # instance attribute (stored in each object)
    self.lastname = lname # instance attribute

  def printname(self):
    print(self.firstname, self.lastname)  # prints first and last name

#Use the Person class to create an object, then execute the printname method:

x = Person("John", "Doe")  # object created, __init__ runs automatically
x.printname()              # Output: John Doe


#example 2:
class Person:
  def __init__(self, name, age):
    self.name = name # stored inside object
    self.age = age # stored inside object

p1 = Person("Emil", 36) # new object, different class definition (overwrites previous Person)

print(p1.name)  # Output:Emil
print(p1.age) # Output:36


#example 3:
#You can access object properties using dot notation
class Car:
  def __init__(self, brand, model):
    self.brand = brand # attribute
    self.model = model # attribute

car1 = Car("Toyota", "Corolla") # object creation

print(car1.brand) # Output: Toyota
print(car1.model) # Output: Corolla
