with open("sample.txt", "r") as file:
    text = file.read()   # read() reads the whole file as one string

print("File content:")
print(text)