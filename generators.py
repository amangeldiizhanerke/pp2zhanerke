# exercise 1:
# generator that generates the squares of numbers up to some number N
n = int(input())

def squares_up_to_n(n):
    for i in range(n + 1):   # включаем n
        yield i**2

for num in squares_up_to_n(n):
    print(num)


# exercise 2:
# print the even numbers between 0 and n in comma separated form
y = int(input())

def even_numbers(y):
    for i in range(y + 1):
        if i % 2 == 0:
            yield i

print(",".join(str(num) for num in even_numbers(y)))


# exercise 3:
# numbers divisible by 3 and 4 between 0 and n
b = int(input())

def divisible_by_3_and_4(b):
    for i in range(b + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

print(",".join(str(num) for num in divisible_by_3_and_4(b)))


# exercise 4:
# generator called squares to yield the square of all numbers from (a) to (b)
f = int(input())
g = int(input())

def squares(f, g):
    for i in range(f, g + 1):
        yield i**2

for num in squares(f, g):
    print(num, end=" ")

print()  # чтобы следующий вывод начался с новой строки


# exercise 5:
# generator that returns all numbers from (n) down to 0
k = int(input())

def countdown(k):
    for i in range(k, -1, -1):
        yield i

for num in countdown(k):
    print(num, end=" ")