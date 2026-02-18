#example 1:
#Create a class named MyClass, with a property named x:
class MyClass:
  x = 5

#example 2:
#Now we can use the class named MyClass to create objects:
p1 = MyClass()
print(p1.x)

#example 3:
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)
#Each object is independent and has its own copy of the class properties