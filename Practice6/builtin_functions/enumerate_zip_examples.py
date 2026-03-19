names = ["Aida", "Nurlan", "Dias"]
ages = [18, 19, 20]

print("Enumerate:")
for i, name in enumerate(names):
    # enumerate gives index + value
    print(i, name)

print("\nZip:")
for name, age in zip(names, ages):
    # zip pairs elements from two lists
    print(name, age)

x = "50"

print("\nBefore:", type(x))

x = int(x)   # convert string to integer

print("After:", type(x))
print("x + 5 =", x + 5)