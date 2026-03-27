#exercise 1:
#generator that generates the squares of numbers up to some number N
n = int(input())
def my_generator(n):
    for i in range(n + 1):
        yield i**2
        
for num in my_generator(n):
    print(num)


#exercise 2:
#print the even numbers between 0 and n in comma separated form where n is input from console
y = int(input())
def my_generator2(y):
    for i in range(y + 1):
        if i % 2 == 0:
            yield i

print(",".join(str(num) for num in my_generator2(y)))

#exercise 3:
#function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n
b = int(input())
def my_generator3(b):
    for i in range(b + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

print(",".join(str(num) for num in my_generator3(b)))


#exercise 4:
#generator called squares to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values
f, g = input().split()
f = int(f)
g = int(g)

def squares(f, g):
    for i in range(f, g + 1):
        yield i**2
        
for num in squares(f, g):
    print(num, end=" ")
print ()

#exercise 5:
#generator that returns all numbers from (n) down to 0
k = int(input())
def noname(k):
    for i in range(k, -1, -1):
        yield i
        
for num in noname(k):
    print(num, end=" ")