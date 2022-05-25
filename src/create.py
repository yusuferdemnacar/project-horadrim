from createFile import create_file

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
    
    create_file("000", rel_name, field_count, pk_order)
    
    return 0

def create_record():

    pass

if(__name__ == "__main__"):

    print(create_type("evil", 4, 1, [["name", "string"],["type", "string"],["alias", "string"],["spell", "string"]]))