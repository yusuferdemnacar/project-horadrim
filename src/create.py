from createFile import create_file
from bplustree import *
import os

## Fields are an array of strings/integers
def insert_record(filename, fields, pkOrder):

    dataFile = open("./db/" + filename, "r+")

    ## Getting the available pages info from header
    dataFile.seek(25)
    availability = dataFile.read(1)
    availability = int(availability, 16)

    ## If there is no available pages, continue
    if availability == 0:
        dataFile.close()
        return False
            

    ## Getting the page to insert            
    pageToInsert = -1
    availability = bin(availability)[2:].rjust(4, "0")
    for i in range(len(availability)):
        if availability[i] == "1":
            pageToInsert = i
            break

    ## Getting a line to insert
    dataFile.seek(29 + pageToInsert * 1931)
    
    availableLines = dataFile.read(2)
    availableLines = int(availableLines, 16)
    availableLines = bin(availableLines)[2:]
    availableLines = availableLines.rjust(8, "0")
    
    lineToInsert = 0
    for i in range(8):
        if availableLines[i] == "0":
            lineToInsert = i
            break
    
    ## Setting the inserted line to occupied in page header

    availableLines = availableLines[:lineToInsert] + "1" + availableLines[lineToInsert + 1:]
    
    ## Checking if the page will be full after insertion
    pageFilled = False
    if availableLines == "11111111":
        pageFilled = True
    
    dataFile.seek(25)

    ## If the page is filled, change the file header so that it does not show in available pages
    if pageFilled:
        availability = availability[:pageToInsert] + "0" + availability[pageToInsert + 1:]
        dataFile.write(hex(int(availability, 2))[2:])

    ## Increment the number of records
    dataFile.seek(26)
    numOfRecords = dataFile.read(2)
    numOfRecords = int(numOfRecords, 16)
    numOfRecords = numOfRecords + 1
    numOfRecords = hex(numOfRecords)
    numOfRecords = (numOfRecords[2:]).rjust(2,"0")
    dataFile.seek(26)
    dataFile.write(numOfRecords)
    

    dataFile.seek(29 + pageToInsert*1931)
    dataFile.write((hex(int(availableLines, 2))[2:]).rjust(2,"0"))
    dataFile.seek(29 + pageToInsert*1931 + 3 + lineToInsert*241)
    for i in fields:
        dataFile.write(i.ljust(20))

    dataFile.close()
    
    ## Add the address to the B+ tree file of the type
    treef = open("./db/" + filename[:-4] + "_tree", "a")
    treef.write(fields[int(pkOrder)] + ":" + filename[-3:] + str(pageToInsert) + str(lineToInsert) + "\n")
    treef.close()
    
    return True

def create_type(rel_name, field_count, pk_order, field_specs):
    
    # Replace "string" with "s" and "integer" with "i" in field_specs
    
    for field_spec in field_specs:
        if field_spec[1] == "string":
            field_spec[1] = "s"
        else:
            field_spec[1] = "i"
    
    # Check the system catalog if there is a relation with the given name
    # Return 1 if there is a relation with the given name

    syscatf = open("./db/syscat", "r")
    
    i=20
    relation_name = "#"
    while(len(relation_name) != 0):
        syscatf.seek(i)
        relation_name = syscatf.read(20).replace(" ", "")
        if(relation_name == rel_name):
            syscatf.close()
            return 1
        i += 43+1
    syscatf.close()
    
    # Add the new relation to the system catalog
    
    syscatf = open("./db/syscat", "a")
    for i in range(field_count):
        if(i + 1 == pk_order):
            pk_status = "p"
        else:
            pk_status = "n"
        syscatf.write(field_specs[i][0].ljust(20) + rel_name.ljust(20) + field_specs[i][1] + hex(i)[2:] + pk_status + "\n")
    syscatf.close()
    
    # Create filecon if not exists,
    # Add relation to filecon
    
    fileconf = open("./db/filecon", "a")
    fileconf.write(rel_name.ljust(20) + "000\n")
    
    # Create the first file for the newly created relation
    
    create_file("000", rel_name, field_count, pk_order - 1)
    
    # Create the index file that will store the b plus tree
    
    treef = open("./db/" + rel_name + "_tree", "w")
    treef.close
    
    return 0

## Fields are an array of strings/integers
def create_record(type_name, fields):

    ## Check if the type exists
    ## If exists, get the primary key order

    syscatf = open("./db/syscat", "r")
    syscatLines = syscatf.readlines()
    syscatf.close()

    typeSyscatLines = []

    for i in range(len(syscatLines)):
        if syscatLines[i][20:40] == type_name.ljust(20):
            typeSyscatLines.append(syscatLines[i])
    
    ## Return error if the type does not exist
    if len(typeSyscatLines) == 0:
        return 1
    

    field_count = len(typeSyscatLines)
    pkOrder = -1
    for line in typeSyscatLines:
        if line[42:43] == "p":
            pkOrder = line[41:42]
            break

    ## If there is no primary key somehow, return error
    if pkOrder == -1:
        return 1


    ## Search for the files designated for the given type
    files = os.listdir("./db")
    type_files = []
    for i in files:
        if ((type_name + "_") in i) and ("tree" not in i[i.index("_") + 1:]):
            type_files.append(i)
            
    #### If there are no files for the record

    ## Get the next file index from filecon
    if len(type_files) == 0:
        fileconf = open("./db/filecon", "r")
        fileconfLines = fileconf.readlines()
        fileconf.close()
        file_index = "000"
        index_position = 0
        for i in range(len(fileconfLines)):
            if fileconfLines[i][0:20] == type_name.ljust(20):
                file_index = fileconfLines[i][20:23]
                index_position = i
                break

        
        ## Incrementing file index
        fileconf = open("./db/filecon", "r+")
        fileconf.seek(index_position*23+20)

        file_index = int(file_index, 16)
        file_index = file_index + 1
        file_index = hex(file_index)
        file_index = (file_index[2:]).rjust(3,"0")

        fileconf.write(file_index)
        fileconf.close()
        
        create_file(file_index, type_name, field_count, int(pkOrder))
        insert_record(type_name + "_" + file_index, fields, int(pkOrder))

    #### If there are existing files for this typename
    else:
        spot_found = False

        ## Checking and inserting if existing files are available for insertion
        for i in type_files:
            
            spot_found = insert_record(i, fields, int(pkOrder))
            if spot_found:
                break
        
        ## If there are no empty spaces in existing files
        ## Then create a new file
        if not spot_found:
            fileconf = open("./db/filecon", "r")
            fileconfLines = fileconf.readlines()
            fileconf.close()
            file_index = "000"
            index_position = 0
            for i in range(len(fileconfLines)):
                if fileconfLines[i][0:20] == type_name.ljust(20):
                    file_index = fileconfLines[i][20:23]
                    index_position = i
                    break

            
            ## Incrementing file index
            fileconf = open ("./db/filecon", "r+")
            fileconf.seek(index_position*23+20)

            file_index = int(file_index, 16)
            file_index = file_index + 1
            file_index = hex(file_index)
            file_index = (file_index[2:]).rjust(3,"0")

            fileconf.write(file_index)
            fileconf.close()

            ## Creating a new file and then inserting the record
            create_file(file_index, type_name, field_count, int(pkOrder))
            insert_record(type_name + "_" + file_index, fields, int(pkOrder))

    return 0

if(__name__ == "__main__"):
    
    #print(create_type("evil", 4, 1, [["name", "string"],["type", "string"],["alias", "string"],["spell", "string"]]))
    for i in range(1):
        print(create_record("evil", ["Noxar" + str(i), "Ghoul", "Spectre", "Paranoia"]))
