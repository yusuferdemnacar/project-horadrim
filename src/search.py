def search_record(type_name, primary_key, btrees, outputf):
    
    ## Get the type names from system catalog file
    ## And insert them into the set record_types
    syscatf = open("./db/syscat", "r", newline="")
    lines = syscatf.readlines()
    record_types = set()
    for i in range(len(lines)):
        if lines[i][20:40] != "systemCatalog".ljust(20):
            record_types.add(lines[i][20:40].replace(" ",""))
    syscatf.close()

    ## If there is no type with given name, the operation is unsuccessful
    if type_name not in record_types:
        return 1
        
    ## Retrieve the address of the record
        
    address = btrees[type_name].retrieve(primary_key)
    
    ## If there is no such record, return 1
    
    if address is None:
        return 1

    ## If there is, get the address
    file_index = address[0][:3]
    page_index = int(address[0][3])
    record_index = int(address[0][4])

    dataFile = open("./db/" + type_name + "_" + file_index, "r+", newline="")

    ## Remove the whitespaces and return the fields in order
    dataFile.seek(29 + page_index*1931 + 3 + record_index*241)
    fieldsString = dataFile.read(240)
    
    #### Write this value to the output ####
    values = fieldsString.split()
    outputf.write(" ".join(map(str, values)) + "\n")
    outputf.flush()
    #### Write this value to the output ####

    return 0

if __name__=="__main__":

    pass
