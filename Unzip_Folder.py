import zipfile, sys 

ZIP_LOC = ""
UNZIP_LOC = ""

def Unzipping(ZIP_LOC, UNZIP_LOC):
    '''
    ZIP_LOC Path where ZIP folder is present.
    UnZIP_LOC Path where folder will be extracted.
    '''
    
    try:

        with zipfile.ZipFile(ZIP_LOC) as ZIP:
            ZIP.extractall(UNZIP_LOC)

        print("Unzipping Done...")

    except Exception as err:
        print(err)
        sys.exit(1)

Unzipping(ZIP_LOC,UNZIP_LOC)