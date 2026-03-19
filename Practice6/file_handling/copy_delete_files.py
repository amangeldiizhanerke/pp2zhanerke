import shutil
import os

shutil.copy("sample.txt", "sample_copy.txt")
shutil.copy("sample.txt", "sample_backup.txt")  # backup = extra saved copy

file_name = "sample_copy.txt"

if os.path.exists(file_name):
    os.remove(file_name)   # remove() deletes the file
    print("Copied file was deleted")
else:
    print("File was not found")