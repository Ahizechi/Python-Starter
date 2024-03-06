import os

def rename_file(original_name, new_name):
    try:
        os.rename(original_name, new_name)
        print(f"File renamed from {original_name} to {new_name}")
    except FileNotFoundError:
        print("File not found.")

# Test the function
original_filename = 'old_file.txt'
new_filename = 'new_file.txt'
rename_file(original_filename, new_filename)
