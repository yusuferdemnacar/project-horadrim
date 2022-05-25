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

def list_records():

    pass

if __name__=="__main__":

    list_types("output.txt")

    pass
