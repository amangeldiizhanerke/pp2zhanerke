# The "elif" keyword is used when the previous condition is false
# The else statement is executed when the if condition (and any elif conditions) evaluate to False
# The else statement must come last. You cannot have an elif after an else.
# Example 1:
a = 200
b = 33

if b > a:
    print("b is greater than a")
elif a == b:
    print("a and b are equal")
else:
    print("a is greater than b")  # prints a is greater than b

# Example 2:
a = 200
b = 33

if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")  # prints b is not greater than a


# Example 3:
number = 7

if number % 2 == 0:
    print("The number is even")
else:
    print("The number is odd")  # prints The number is odd

# Example 4:
temperature = 22

if temperature > 30:
    print("It's hot outside!")
elif temperature > 20:
    print("It's warm outside")  # prints It's warm outside
elif temperature > 10:
    print("It's cool outside")
else:
    print("It's cold outside!")


# Example 5:
# Validating user input

username = "Emil"

if len(username) > 0:
    print(f"Welcome, {username}!")  # prints Welcome, Emil!
else:
    print("Error: Username cannot be empty")
