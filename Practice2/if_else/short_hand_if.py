#Short hand if is used to write an if statement in one line
#It is used when there is only one statement to execute
#Example 1:
a = 33
b = 200
if a > b: print("a is greater than b")

#Example 2:
a = 33
b = 200
print("A") if a > b else print("B")

#Example 3 (multiple conditions in one line):
a = 33
b = 200
print("A") if a > b else print("=") if a == b else print("B")
