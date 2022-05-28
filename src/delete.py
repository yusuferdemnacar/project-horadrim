import os

def delete_type(type_name):

    syscatf = open("./db/syscat", "r")
    lines = syscatf.readlines()
    syscatf.close()
    linesToDelete = []

    # Check which lines will be deleted from system catalog
    
    for i in range(len(lines)):
        if lines[i][20:40] == type_name.ljust(20):
            linesToDelete.append(i)
    
    # If the type does not exist in the system, return error

    if len(linesToDelete) == 0:
        return 1
        
    # Deleting the lines for the type from system catalog
    
    syscatf = open("./db/syscat", "w")
    for i in range(len(lines)):
        if i not in linesToDelete:
            syscatf.write(lines[i])

    # Deleting the files that store information for this type
    
    files = os.listdir("./db")
    for i in files:
        if (type_name + "_") in i:
            os.remove("./db/" + i)

    # Deleting the info of this type in filecon
    
    fileconf = open("./db/filecon", "r")
    lines = fileconf.readlines()
    fileconf.close()
         
    fileconf = open("./db/filecon", "w")
    
    for line in lines:
        if line[0:20] != type_name.ljust(20):
            fileconf.write(line)
            
    fileconf.close()
    
    return 0

def delete_record(type_name, primary_key, btrees):
    
    ## If there is an error, the function shall return 1
    
    ## Retrieve the address of the record, if there is no record, return 1

    address = btrees[type_name].retrieve(primary_key)
    
    if address is None:
        return 1
    
    file_index = address[:3]
    page_index = int(address[3])
    record_index = int(address[4])
    ## This variables hold the values returned from the B+ tree
    
    dataFile = open("./db/" + type_name + "_" + file_index, "r+")

    ## Decrementing the amount of total records info from file header
    ## If there are 0 records left, delete the file
    dataFile.seek(26)
    numOfRecords = dataFile.read(2)
    numOfRecords = int(numOfRecords, 16)
    numOfRecords = numOfRecords - 1
    if numOfRecords == 0:
        dataFile.close()
        os.remove("./db/" + type_name + "_" + file_index)
        return 0
    numOfRecords = hex(numOfRecords)[2:].rjust(2, "0")
    dataFile.seek(26)
    dataFile.write(numOfRecords)

    ## Modifying the available pages info if the page that 
    ## We are going to delete from is full
    dataFile.seek(25)
    availablePages = dataFile.read(1)
    availablePages = int(availablePages, 16)
    availablePages = bin(availablePages)[2:].rjust(4, "0")
    if availablePages[page_index] == 0:
        availablePages = availablePages[:page_index] + "1" + availablePages[page_index + 1:]
        dataFile.seek(25)
        dataFile.write(hex(int(availablePages, 2))[2:])

    ## Modifying the available lines from page header since
    ## We are going to remove a record
    dataFile.seek(29 + page_index*1931)
    availableLines = dataFile.read(2)
    availableLines = int(availableLines, 16)
    availableLines = bin(availableLines)[2:]
    availableLines = availableLines.rjust(8, "0")
    availableLines = availableLines[:record_index] + "0" + availableLines[record_index + 1:]
    dataFile.seek(29 + page_index*1931)
    dataFile.write((hex(int(availableLines, 2))[2:]).rjust(2,"0"))

    ## Overwriting the record with whitespaces
    dataFile.seek(29 + page_index*1931 + 3 + record_index*241)
    dataFile.write(" " * 240)
    
    ## Remove the record from the tree
    
    btrees[type_name].delete(primary_key)

    return 0

if __name__=="__main__":
    
    print(delete_record("evil", "Nox"))