import os

os.makedirs("dir1/dir2/dir3", exist_ok=True)
# makedirs() creates nested folders
# exist_ok=True prevents an error if folders already exist

print("Files and folders in current directory:")
for item in os.listdir("."):
    print(item)

print("\nTXT files:")
for item in os.listdir("."):
    if item.endswith(".txt"):   # endswith(".txt") checks file extension
        print(item)