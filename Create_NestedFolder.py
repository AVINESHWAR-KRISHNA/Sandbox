import os
import random
import string

# Set the base directory
base_dir = ""

# Set the names of the subfolders
subfolder_names = ['FFS01D', 'CPIC01D', 'CPIF01D', 'CPGC01D', 'CPGF01D']

# Create the base directory if it doesn't already exist
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# Create 500 top-level folders
for i in range(1, 501):

    folder_name = ''.join(random.sample(string.ascii_letters, 6))

    # Create the top-level folder
    top_folder = os.path.join(base_dir, folder_name)
    os.makedirs(top_folder)
    
    # Create the subfolders
    for subfolder in subfolder_names:
        os.makedirs(os.path.join(top_folder, subfolder))

print("Folders created successfully!")