class MyClass:
  x = 5   # class variable

p1 = MyClass()
p2 = MyClass()

print(p1.x)
print(p2.x)

MyClass.x = 10   # change class variable

print(p1.x)
print(p2.x)
