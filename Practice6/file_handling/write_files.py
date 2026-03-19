with open("sample.txt", "w") as file:
    # "w" means write mode: it creates a new file or overwrites the old one
    file.write("Name: Aigerim\n")
    file.write("Age: 18\n")
    file.write("City: Almaty\n")

with open("sample.txt", "a") as file:
    # "a" means append mode: it adds new text without deleting old content
    file.write("University: KBTU\n")
    file.write("Major: Petroleum Engineering\n")

print("Data was written to sample.txt")