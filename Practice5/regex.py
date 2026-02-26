import re


# Exercise 1
# match 'a' followed by zero or more 'b'
pattern = r"ab*"
examples = ["a", "ab", "abb", "b"]

for word in examples:
    if re.fullmatch(pattern, word):
        print("1) matched:", word)


# Exercise 2
# match 'a' followed by two to three 'b'
pattern = r"ab{2,3}"
examples = ["a", "ab", "abb", "abbb", "abbbb"]

for word in examples:
    if re.fullmatch(pattern, word):
        print("2) matched:", word)


# Exercise 3
# find lowercase words connected with underscore
text = "hello_world test_case Python_123"
result = re.findall(r"[a-z]+_[a-z]+", text)
print("3)", result)


# Exercise 4
# find words that start with capital letter
text = "Hello World Python CODE Test"
result = re.findall(r"[A-Z][a-z]+", text)
print("4)", result)


# Exercise 5
# match string starting with 'a' and ending with 'b'
pattern = r"a.*b"
examples = ["ab", "acb", "axxxb", "ba"]

for word in examples:
    if re.fullmatch(pattern, word):
        print("5) matched:", word)


# Exercise 6
# replace space, comma and dot with colon
text = "hello, world. python is cool"
new_text = re.sub(r"[ ,\.]", ":", text)
print("6)", new_text)


# Exercise 7
# convert snake_case to camelCase
text = "this_is_example"

parts = text.split("_")
camel = parts[0]

for part in parts[1:]:
    camel += part.capitalize()

print("7)", camel)


# Exercise 8
# split string at uppercase letters
text = "HelloWorldPython"
words = re.findall(r"[A-Z][a-z]*", text)
print("8)", words)


# Exercise 9
# insert spaces before capital letters
text = "HelloWorldPython"
spaced = re.sub(r"([A-Z])", r" \1", text).strip()
print("9)", spaced)


# Exercise 10
# convert camelCase to snake_case
text = "thisIsCamelCase"

snake = re.sub(r"([A-Z])", r"_\1", text)
snake = snake.lower()

print("10)", snake)