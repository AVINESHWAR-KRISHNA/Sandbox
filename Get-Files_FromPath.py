import os,sys
import pandas as pd


_dir = '_SrcLoc'

DFs = {}
SrcFilePaths = {}


try:      
    print("Looking for file in dir.") 
    Files = os.listdir(_dir)
    
    __ln = []

    if len(Files) != 0:        
        for i in range(len(Files)):
            if Files[i].endswith('.csv'):
                __ln.append(Files[i])  

        if len(__ln) != 0:     
     
            file = __ln.pop()
            DFs[file.split('.csv')[0]] = pd.read_csv(f"{_dir+file}",encoding= 'unicode_escape')
            SrcFilePaths[file.split('.csv')[0]] = f"{_dir+file}"
            
    if bool(DFs) == False:
        print("No file found.")
        
    else:
        print(f"File found :: {DFs.keys()}")

        
    
except Exception as err:
    print("Error while parsing file.")
    print("sys exit")

    sys.exit(1)