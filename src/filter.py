def filter_records(type_name, condition):
    ## Use the B+ tree and parse the condition string to get the
    ## desired addresses from the B+ tree, if there is an error
    ## doing so, or there are 0 addresses, return 1

    file_index_arr = ["000","001"]
    page_index_arr = [0,0]
    record_index_arr = [0,0]
    valueList = []

    ## Get the fields of all received addresses from the tree
    for i in range(len(file_index_arr)):
        file_index = file_index_arr[i]
        page_index = page_index_arr[i]
        record_index = record_index_arr[i]

        dataFile = open("./db/" + type_name + "_" + file_index)
        dataFile.seek(29 + page_index*1931 + 3 + record_index*241)
        fieldsString = dataFile.read(240)
        valueList.append(fieldsString.split())

    #### Now the function must write the valueList array to the output file ####
    return 0

if __name__=="__main__":

    pass
