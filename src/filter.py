from bplustree import *

def filter_records(type_name, condition, trees, outputf):
    
    ## Check if the type exists
    ## If exists, get the primary key type

    syscatf = open("./db/syscat", "r", newline="")
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
    pk_field_type = ""
    for line in typeSyscatLines:
        if line[42:43] == "p":
            pk_field_type = line[40]
            break
    
    current_node = trees[type_name].root
    
    is_leaf = False
    
    primary_key = ""
    cond_key = ""
    operator = ""
    
    if ((operator := "<") in condition) or ((operator := "=") in condition) or ((operator := ">") in condition):
        primary_key = condition[:condition.index(operator)]
        if pk_field_type == "s":
            cond_key = condition[condition.index(operator) + 1:]
        else:
            cond_key = int(condition[condition.index(operator) + 1:])
    
    keys = []
    address_arr = []
    file_index_arr = []
    page_index_arr = []
    record_index_arr = []
    
    first_node = True
    flip = True
    
    while not is_leaf:
    
        if operator == "<":
            
            if isinstance(current_node.values[0], list):
                is_leaf = True
                cnode = current_node
                while cnode is not None:
                    for k in reversed(cnode.keys):
                        if (not first_node) or (k < cond_key):
                            keys.append(k)
                            address_arr.append(cnode.values[cnode.keys.index(k)][0])
                    cnode = cnode.prevLeaf
                    first_node = False
            else:
                next_node_index = 0
                for comp_key in current_node.keys:
                    if comp_key <= cond_key:
                        next_node_index += 1
                current_node = current_node.values[next_node_index]
                
        elif operator == ">":
            flip = False
            if isinstance(current_node.values[0], list):
                is_leaf = True
                cnode = current_node
                while cnode is not None:
                    for k in cnode.keys:
                        if (not first_node) or (k > cond_key):
                            keys.append(k)
                            address_arr.append(cnode.values[cnode.keys.index(k)][0])
                    cnode = cnode.nextLeaf
                    first_node = False
            else:
                next_node_index = len(current_node.keys)
                for comp_key in reversed(current_node.keys):
                    if comp_key >= cond_key:
                        next_node_index -= 1
                current_node = current_node.values[next_node_index]
                
        elif operator == "=":
    
            if isinstance(current_node.values[0], list):
                is_leaf = True
                if cond_key in current_node.keys:
                    keys.append(cond_key)
                    address_arr.append(current_node.values[current_node.keys.index(cond_key)][0])
            else:
                next_node_index = 0
                for comp_key in current_node.keys:
                    if comp_key <= cond_key:
                        next_node_index += 1
                current_node = current_node.values[next_node_index]
    
    if flip:
        address_arr.reverse()
        
    for address in address_arr:
        file_index_arr.append(address[:3])
        page_index_arr.append(int(address[3]))
        record_index_arr.append(int(address[4]))  

    valueList = []

    ## Get the fields of all received addresses from the tree
    for i in range(len(file_index_arr)):
        file_index = file_index_arr[i]
        page_index = page_index_arr[i]
        record_index = record_index_arr[i]

        dataFile = open("./db/" + type_name + "_" + file_index, "r+", newline="")
        dataFile.seek(29 + page_index*1931 + 3 + record_index*241)
        fieldsString = dataFile.read(240)
        valueList.append(fieldsString.split())

    #### Now the function must write the valueList array to the output file ####
    
    if len(valueList) == 0:
        return 1
    
    for value in valueList:
        outputf.write(" ".join(map(str, value)) + "\n")
    
    outputf.flush()
    
    return 0

if __name__=="__main__":

    pass
