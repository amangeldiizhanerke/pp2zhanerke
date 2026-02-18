#example 1:
#Create a method in a class:
#All methods must have self as the first parameter.
class Person:
  def __init__(self, name):
    self.name = name

  def greet(self):
    print("Hello, my name is " + self.name)

p1 = Person("Emil")   # object is created, __init__ runs automatically
p1.greet()            # Output: Hello, my name is Emil


#example 2:
#Methods can accept parameters just like regular functions:
class Calculator:
  def add(self, a, b):
    return a + b     

  def multiply(self, a, b):
    return a * b       

calc = Calculator() # create Calculator object
print(calc.add(5, 3)) # Output: 8
print(calc.multiply(4, 7)) # Output: 28


#example 3:
#You can delete methods from a class using the del keyword:
class Person:
  def __init__(self, name):
    self.name = name

  def greet(self):
    print("Hello!")

p1 = Person("Emil") # create object
del Person.greet # removes greet method from the class
p1.greet() # Error: AttributeError (method no longer exists)
