import shutil
import os

os.makedirs("dir1", exist_ok=True)

if os.path.exists("sample.txt"):
    shutil.copy("sample.txt", "dir1/sample_copy.txt")
    print("File was copied to dir1")

if os.path.exists("sample.txt"):
    shutil.move("sample.txt", "dir1/sample_moved.txt")
    # move() cuts the file from old place and puts it into a new one
    print("File was moved to dir1")