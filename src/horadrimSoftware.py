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

inputf = open(sys.argv[1], "r", newline="")

input_lines = inputf.read().splitlines()

inputf.close()

# Create the output file

outputf = open(sys.argv[2], "a", newline="")

# Create the log file

logf = open("horadrimLog.csv", "a", newline="")

# Dictionary for the tree objects

trees = {}

# Create db folder if not exists

if not os.path.exists("./db"):

    os.mkdir("./db")

# Create syscat file if not exists

if not os.path.exists("./db/syscat"):

    syscatf = open("./db/syscat", "w", newline="")

    # write the metadata for the syscat table itself

    syscatf.write("attributeName       systemCatalog       s0n\n")
    syscatf.write("relationName        systemCatalog       s1n\n")
    syscatf.write("type                systemCatalog       s2n\n")
    syscatf.write("position            systemCatalog       s3n\n")
    syscatf.write("ispk                systemCatalog       s4n\n")
    
    syscatf.close()

# Read the syscat to get primary field types for tree reconstruction

syscatf = open("./db/syscat", "r", newline="")
syscatlines = syscatf.read().splitlines()

pk_field_types = {}

for syscatline in syscatlines:
    if syscatline[42] == "p":
        pk_field_types[syscatline[20:40].replace(" ", "")] = syscatline[40]

# Open the tree files and reconstruct the trees

dbfiles = os.listdir("./db")
for file in dbfiles:
    if "_tree" in file:
        typename = file[:file.index("_")]
        field_type = pk_field_types[typename]
        trees[typename] = BPlusTree(order=4)
        trees[typename].deserializeTree(typename, field_type)
    
for line in input_lines:
    
    tokens = line.split()
    
    if tokens[0] == "create":
        
        if tokens[1] == "type":
        
            # Prepare the arguments
        
            field_specs = []
        
            for i in range(5, len(tokens) - 1, 2):
                field_specs.append([tokens[i], tokens[i+1]])
                
            # Try to create type
            
            is_successful = create_type(tokens[2], int(tokens[3]), int(tokens[4]), field_specs)
            
            # If a type is created, create a tree for it
            
            if is_successful == 0:
            
                trees[tokens[2]] = BPlusTree(order=4)
                
            # Log the type creation

            logf.write(str(int(time.time())) + "," + line + "," + ("success" if is_successful == 0 else "failure") + "\n")
            logf.flush()
            
        elif tokens[1] == "record":
        
            # Prepare the arguments
        
            fields = []
        
            for i in range(3, len(tokens)):
                fields.append(tokens[i])
                
            # Try to create record
        
            is_successful = create_record(tokens[2], fields, trees)
            
            # Log the record creation
            
            logf.write(str(int(time.time())) + "," + line + "," + ("success" if is_successful == 0 else "failure") + "\n")
            logf.flush()
        
    elif tokens[0] == "delete":
    
        if tokens[1] == "type":
        
            # Try to delete type
            
            is_successful = delete_type(tokens[2])
            
            # If a type is deleted, delete its tree
            
            if is_successful == 0:
                
                trees.pop(tokens[2])
                
            # Log the type deletion
                
            logf.write(str(int(time.time())) + "," + line + "," + ("success" if is_successful == 0 else "failure") + "\n")
            logf.flush()
            
        elif tokens[1] == "record":
        
            # Try to delete record
            
            is_successful = delete_record(tokens[2], tokens[3], trees)
            
            # Log the record deletion
            
            logf.write(str(int(time.time())) + "," + line + "," + ("success" if is_successful == 0 else "failure") + "\n")
            logf.flush()
            
    elif tokens[0] == "list":
    
        if tokens[1] == "type":
            
            # Try to list types
            
            is_successful = list_types(sys.argv[2])
            
            # Log the type listing
            
            logf.write(str(int(time.time())) + "," + line + "," + ("success" if is_successful == 0 else "failure") + "\n")
            logf.flush()
            
        elif tokens[1] == "record":
        
            # Try to list records
        
            is_successful = list_records(tokens[2], trees, outputf)
            
            # Log the record listing
            
            logf.write(str(int(time.time())) + "," + line + "," + ("success" if is_successful == 0 else "failure") + "\n")
            logf.flush()

    elif tokens[0] == "search":
    
        # Try to search record
    
        is_successful = search_record(tokens[2], tokens[3], trees, outputf)
        
        # Log the record search
        
        logf.write(str(int(time.time())) + "," + line + "," + ("success" if is_successful == 0 else "failure") + "\n")
        logf.flush()

    elif tokens[0] == "update":
    
        # Prepare the arguments

        fields = []
        
        for i in range(4, len(tokens)):
            fields.append(tokens[i])

        # Try to update record
        
        is_successful = update_record(tokens[2], tokens[3], fields, trees)
        
        # Log the record update
        
        logf.write(str(int(time.time())) + "," + line + "," + ("success" if is_successful == 0 else "failure") + "\n")
        logf.flush()
        
    elif tokens[0] == "filter":
    
        # Try to filter records
    
        is_successful = filter_records(tokens[2], tokens[3], trees, outputf)
        
        # Log the filtering
        
        logf.write(str(int(time.time())) + "," + line + "," + ("success" if is_successful == 0 else "failure") + "\n")
        logf.flush()

# Save the trees in files

for treekey in trees.keys():
    trees[treekey].serializeTree(treekey)