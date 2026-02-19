#Example 1:
#The __init__() function is called automatically every time
#the class is being used to create a new object.

class Person:
  def __init__(self, fname, lname):
    self.firstname = fname # instance attribute (stored in each object)


  def printname(self):
    print(self.firstname, self.lastname)

x = Person("John", "Doe") # object created, __init__ runs automatically
x.printname() # Output: John Doe

#example 2:
#You can access object properties using dot notation
class Car:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

car1 = Car("Toyota", "Corolla")

print(car1.brand) #Output: Toyota
print(car1.model) #Output: Corolla
