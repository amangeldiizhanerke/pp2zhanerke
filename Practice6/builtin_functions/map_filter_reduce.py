from functools import reduce

nums = [1, 2, 3, 4]

# map: add 1 to each number
new_nums = list(map(lambda x: x + 1, nums))
print("Map result:", new_nums)

# filter: keep numbers greater than 2
big_nums = list(filter(lambda x: x > 2, nums))
print("Filter result:", big_nums)

# reduce: sum all numbers
total = reduce(lambda a, b: a + b, nums)
print("Sum:", total)