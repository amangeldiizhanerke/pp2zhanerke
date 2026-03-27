#exercise 1:
#a Python program to subtract five days from current date
import datetime #import a module named datetime to work with dates as date objects
x = datetime.datetime.now()
print(x - datetime.timedelta(days=5))

#exercise 2:
#a Python program to print yesterday, today, tomorrow
x = datetime.datetime.now()
print(x - datetime.timedelta(days=1))
print(x)
print(x + datetime.timedelta(days=1))

#exercise 3:
#a Python program to drop microseconds from datetime
x = datetime.datetime.now().replace(microsecond=0)
print(x)

#exercise 4:
#a Python program to calculate two date difference in seconds
x = datetime.datetime(2025, 1, 1)
y = datetime.datetime(2025, 1, 2)
z = y - x
print(z.total_seconds()) #convert time difference to seconds