#!/usr/bin/env python
#Reduce function for computing matrix multiply A*B

import sys

# Create data structures to hold the current row/column values 

###
# (if needed; your code goes here)
###
current_key = None
dictA = {}
dictB = {}

# input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:

    # Remove leading and trailing whitespace
    line = line.strip()

    # Get key/value and split by tab
    key, value = line.split('\t', 1)

    # Parse key/value input (your code goes here)

    # If we are still on the same key...
    if key == current_key:
      
        # Process key/value pair

        ###
        # (your code goes here)
        if value.split('|')[0] == 'A':
            dictA[value.split('|')[1]] = value.split('|')[2]
                     
        if value.split('|')[0] == 'B':
            dictB[value.split('|')[1]] = value.split('|')[2]

                  

    # Otherwise, if this is a new key...
    else:
        # If this is a new key and not the first key we've seen
        if current_key:
            #compute/output result to STDOUT

            ###
            # (your code goes here)
            print('{}\t{}'.format(current_key,sum([int(dictA[pos])*int(dictB[pos]) for pos in dictA.keys()])))
            dictA ={}
            dictB ={}
            
         
        if value[0] == 'A':
            dictA[value.split('|')[1]] = value.split('|')[2]
         
        if value.split('|')[0] == 'B':
            dictB[value.split('|')[1]] = value.split('|')[2]
        
        current_key  = key
        
#Compute/output result for the last key

###
# (your code goes here)
if current_key != None: 
    print('{}\t{}'.format(current_key,sum([int(dictA[pos])*int(dictB[pos]) for pos in dictA.keys()])))
    dictA ={}
    dictB ={}
# ###