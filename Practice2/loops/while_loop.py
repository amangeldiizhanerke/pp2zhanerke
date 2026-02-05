#With the while loop we can execute a set of statements as long as a condition is true
#Example 1
i = 1
while i < 6:
  print(i)
  i += 1

#With the else statement we can run a block of code once when the condition no longer is true:
#Example 2
i = 1
while i < 6:
  print(i)
  i += 1
else:
  print("i is no longer less than 6")