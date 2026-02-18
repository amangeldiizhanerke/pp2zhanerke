class Person:
  def greet(self):
    print("Hello from Person")

class Student(Person):
  def greet(self):   # overriding the parent method
    print("Hello from Student")

p = Person()
s = Student()

p.greet()  # Output: Hello from Person
s.greet()  # Output: Hello from Student
