def list_types(outputName):

    ## Get the type names from system catalog file
    ## And insert them into the set record_types
    syscatf = open("./db/syscat", "r")
    lines = syscatf.readlines()
    record_types = set()
    for i in range(len(lines)):
        if lines[i][20:40] != "systemCatalog".ljust(20):
            record_types.add(lines[i][20:40])
    syscatf.close()

    ## If there is no type, the operation is unsuccessful
    if len(record_types) == 0:
        return 1

    ## Printing the types to the output file
    outfile = open(outputName, "a")
    for i in record_types:
        outfile.write(i.replace(" ","") + "\n")

    return 0

def list_records(type_name):

    ## Get the following values from B+ Tree
    ## If not, return error
    file_index_arr = ["000","001"]
    page_index_arr = [0,0]
    record_index_arr = [0,0]
    valueList = []

    ## Get the fields of all received addresses from the tree
    for i in range(len(file_index_arr)):
        file_index = file_index_arr[i]
        page_index = page_index_arr[i]
        record_index = record_index_arr[i]

        dataFile = open("./db/" + type_name + "_" + file_index, "r+")
        dataFile.seek(29 + page_index*1931 + 3 + record_index*241)
        fieldsString = dataFile.read(240)
        valueList.append(fieldsString.split())

    #### Now the function must write the valueList array to the output file ####
    return 0

if __name__=="__main__":

    list_types("output.txt")

    pass
