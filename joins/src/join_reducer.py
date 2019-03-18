#!/usr/bin/env python
#Reduce function for join reducer

import sys

current_key = None
term_join_check = False
track_join_check = False
term_values = []
track_values = []

# input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:

    # Remove leading and trailing whitespace
    line = line.strip()
    
    # Get key/value and split by tab
    key, value = line.split('\t', 1)

    # If we are still on the same key...
    if key == current_key:

        if len(value.split(',')) == 1:
            term_values.append(value)
            term_join_check = True
            
        elif len(value.split(',')) == 5: 
            track_values.append(value.split(',')[0])
            track_join_check = True

     # If this is a new key and not the first key we've seen
    elif current_key:

        if term_join_check and track_join_check: 
            for track in track_values: 
                for term in term_values:
                    #compute/output result to STDOUT - artist_id, track_id, term
                    print('{}\t{}'.format(current_key,(track,term)))
                                 
            
        #reset values for the next key
        track_values = []
        term_values = []
        term_join_check = False
        track_join_check = False
            
        #starts grouping for the next key if key != current_key
        if len(value.split(',')) == 1:
            term_values.append(value)
            term_join_check = True
        
        elif len(value.split(',')) == 5: 
            track_values.append(value.split(',')[0])
            track_join_check = True
    
    
    #new key and the first key we've seen
    else:
        if len(value.split(',')) == 1:
            term_values.append(value)
            term_join_check = True
        
        elif len(value.split(',')) == 5: 
            track_values.append(value.split(',')[0])
            track_join_check = True
    
    current_key = key
    current_value = value

#Compute/output result for the last key
###
if term_join_check and track_join_check: 
    for track in track_values: 
        for term in term_values:
            #compute/output result to STDOUT - artist_id, track_id, term
            print('{}\t{}'.format(current_key,(track,term)))
            

###