import fileinput


def search_record(type_name, primary_key):

    ## Get the following values from B+ Tree
    ## If not, return error
    file_index = "000"
    page_index = 0
    record_index = 0

    dataFile = open("./db/" + type_name + "_" + file_index)

    ## Remove the whitespaces and return the fields in order
    dataFile.seek(29 + page_index*1931 + 3 + record_index*241)
    fieldsString = dataFile.read(240)
    
    #### Write this value to the output ####
    values = fieldsString.split()
    #### Write this value to the output ####

    return 0

if __name__=="__main__":

    pass
