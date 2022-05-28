def update_record(type_name, primary_key, fields):
    ## Get the file index, page index and record index
    ## From the B+ Tree into the 3 following variables.
    ## If unsuccessful, return 1
    file_index = "000"
    page_index = 0
    record_index = 0

    dataFile = open("./db/" + type_name + "_" + file_index)

    ## If the number of fields are wrong, return an error
    dataFile.seek(23)
    fieldNumber = dataFile.read(1)
    fieldNumber = int(fieldNumber, 16)
    if fieldNumber != len(fields):
        return 1

    ## Overwriting the record with the new fields
    dataFile.seek(29 + page_index*1931 + 3 + record_index*241)
    for i in fields:
        dataFile.write(i.ljust(20))

    dataFile.close()
    return 0

if __name__=="__main__":

    pass
