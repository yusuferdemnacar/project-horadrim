import os
def delete_type(type_name):

    syscatf = open("./db/syscat", "r")
    lines = syscatf.readlines()
    syscatf.close()
    linesToDelete = []

    ## Check which lines will be deleted from system catalog
    for i in range(len(lines)):
        if lines[i][20:40] == type_name.ljust(20):
            linesToDelete.append(i)
    
    ## If the type does not exist in the system, return error
    if linesToDelete == None:
        return 1
        
    ## Deleting the lines for the type from system catalog
    syscatf = open("./db/syscat", "w")
    for i in range (len(lines)):
        if i not in linesToDelete:
            syscatf.write(lines[i])

    ## Deleting the files that store information for this type
    files = os.listdir("./db")
    for i in files:
        if (type_name+"_") in i:
            os.rmdir("./db/"+i)

    ## Deleting the info of this type in filecon
    fileconf = open("./db/filecon", "r")
    lines = fileconf.readlines()
    
    for i in range(len(lines)):
        if lines[i][0:20] == type_name.ljust(20):
            fileconf.close()
            fileconf = open("./db/filecon", "w")
            for j in range(len(lines)):
                if i != j:
                    fileconf.write(lines[j])
            fileconf.close()
            break



    pass

def delete_record():

    pass

if __name__=="__main__":
    
    pass
