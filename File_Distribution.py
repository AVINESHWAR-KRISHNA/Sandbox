import os
import time
import shutil

StartT = time.time()

filepath = ""
path = ""


global Files_Dropped
Files_Dropped = 0

files = []

for file in os.listdir(filepath):
    files.append(file)

for folder in os.listdir(path):
    if os.path.isdir(os.path.join(path, folder)):

        for subfolder in os.listdir(path+folder):
            subfolder_path = os.path.join(path, folder, subfolder)

            if os.path.isdir(subfolder_path):

                for file in files:
                    file_path = os.path.join(filepath, file)

                    if os.path.isfile(file_path):

                        f = os.path.basename(file_path)
                        if subfolder in f:
                            # print(file_path, subfolder_path)
                            # shutil.copy2(file_path, subfolder_path)
                            
                            Files_Dropped += 1

EndT = time.time()
TTime = EndT - StartT

print("Total Files Placed ::", Files_Dropped)
print("Time Taken ::", round(TTime,2))