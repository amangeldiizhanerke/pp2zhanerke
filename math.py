#exercise 1:
#program to convert degree to radian
import math
a = float(input())
print(math.radians(a))

#exercise 2:
#program to calculate the area of a trapezoid
h = float(input())
c = float(input())
b = float(input())
area=(b+c)/2*h
print(area)

#exercise 3:
#calculate the area of regular polygon
import math
sides = int(input())
length = float(input())
area2 = (sides * length**2) / (4 * math.tan(math.pi / sides))
answer=round(area2)
print(f"The area of the polygon is: {answer}")

#exercise 4:
#calculate the area of a parallelogram
x = float(input())
y = float(input())
result = round((x * y),1)
print(f"The area of parallelogram is: {result}")
