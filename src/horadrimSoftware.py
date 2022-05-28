from create import *
from delete import *
from filter import *
from search import *
from update import *
from list import *
from bplustree import *

import sys
import os
import time

# Read the input file

inputf = open(sys.argv[1], "r")

input_lines = inputf.read().splitlines()

inputf.close()

# Create the output file

outputf = open(sys.argv[2], "w")

# Create the log file

logf = open("horadrimLog.csv", "w")

# Dictionary for the tree objects

trees = {}

# Create db folder if not exists

if not os.path.exists("./db"):

    os.mkdir("./db")

# Create syscat file if not exists

if not os.path.exists("./db/syscat"):

    syscatf = open("./db/syscat", "w")

    # write the metadata for the syscat table itself

    syscatf.write("attributeName       systemCatalog       s0n\n")
    syscatf.write("relationName        systemCatalog       s1n\n")
    syscatf.write("type                systemCatalog       s2n\n")
    syscatf.write("position            systemCatalog       s3n\n")
    syscatf.write("ispk                systemCatalog       s4n\n")
    
    syscatf.close()

# Open the tree files and reconstruct the trees

dbfiles = os.listdir("./db")
for file in dbfiles:
    if "_tree" in file:
        typename = file[:file.index("_")]
        trees[typename] = BPlusTree(order=4)
        trees[typename].deserializeTree(typename)
    
for line in input_lines:
    
    tokens = line.split()
    
    if tokens[0] == "create":
        
        if tokens[1] == "type":
        
            field_specs = []
        
            for i in range(5, len(tokens) - 1, 2):
                field_specs.append([tokens[i], tokens[i+1]])
            
            is_successful = create_type(tokens[2], int(tokens[3]), int(tokens[4]), field_specs)
            
            if is_successful == 0:
            
                # If a type is created, create a tree for it
            
                trees[tokens[2]] = BPlusTree(order=4)

            logf.write(str(int(time.time())) + "," + line + "," + ("success" if is_successful == 0 else "failure") + "\n")
            
        elif tokens[1] == "record":
        
            fields = []
        
            for i in range(3, len(tokens) - 1):
                fields.append(tokens[i])
        
            create_record(tokens[2], fields, trees)
        
    elif tokens[0] == "delete":
    
        if tokens[1] == "type":
            
            pass
            
        elif tokens[1] == "record":
        
            pass
    
    elif tokens[0] == "list":
    
        if tokens[1] == "type":
            
            pass
            
        elif tokens[1] == "record":
        
            pass
    
    elif tokens[0] == "search":
    
        pass

    elif tokens[0] == "update":
    
        pass
        
    elif tokens[0] == "filter":
    
        pass

# Save the trees in files

for treekey in trees.keys():
    trees[treekey].serializeTree(treekey)