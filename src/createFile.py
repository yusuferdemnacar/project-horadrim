def create_file(file_index, rel_name, field_count, pk_order):

    newf = open("./db/" + rel_name + "_" + file_index, "w")
    
    newf.write(file_index + rel_name.ljust(20) + hex(field_count)[2:] + hex(pk_order - 1)[2:] + "f00" + "\n")
    
    for i in range(4):
        newf.write("00\n")
        for ii in range(8):
            newf.write(" " * 240 + "\n")
            
if(__name__ == "__main__"):

    create_file("000", "potion", 3, 2)
