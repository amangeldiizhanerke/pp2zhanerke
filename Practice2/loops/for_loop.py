#A for loop is used to go through each item in a list
#Example 1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)

#Example 2
for x in "banana":
  print(x)

#Using the range() function:
#Example 3
for x in range(6):
  print(x)

#Using the start parameter:
#Example 4
for x in range(2, 6):
  print(x)

#Example 5
for x in range(2, 30, 3):
  print(x)

#The else block runs when the loop finishes normally
#Example 6
for x in range(6):
  print(x)
else:
  print("Finally finished!")

#Example 7
for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!")

#Nested Loops
#Example 8
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:
  for y in fruits:
    print(x, y)
