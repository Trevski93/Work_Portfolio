#!/usr/bin/env python
#Reduce function for group reducer
#final output track.artist_id, max(track.year), avg(track.duration), count(artist_term.term)
#track LEFT JOIN artist_term

import sys

current_key = None
term_join_check = False
track_join_check = False
term_values = []
max_track_year = 0
duration = []
record = 0 

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
            track_year = int(value.split(',')[3])
            if track_year > max_track_year:
                max_track_year = track_year
            duration.append(float(value.split(',')[4]))
            track_join_check = True

     # If this is a new key and not the first key we've seen
    elif current_key:

        if track_join_check: 
            #compute/output result to STDOUT - track.artist_id, max(track.year), avg(track.duration),count(artist_term.term) 
            if term_join_check:
                term_count = sum([1 for i in term_values])*len(duration)
                print('{}\t{}'.format(current_key,(max_track_year,sum(duration)/len(duration),term_count)))
                      
            else:
                print('{}\t{}'.format(current_key,(max_track_year,sum(duration)/len(duration),0)))
             
        #reset values for the next key
        term_values = []
        term_join_check = False
        track_join_check = False
        max_track_year = 0
        duration = []
            
        #starts grouping for the next key if key != current_key
        if len(value.split(',')) == 1:
            term_values.append(value)
            term_join_check = True
        
        elif len(value.split(',')) == 5: 
            track_year = int(value.split(',')[3])
            if track_year > max_track_year:
                max_track_year = track_year
            duration.append(float(value.split(',')[4]))
            track_join_check = True
    
    
    #new key and the first key we've seen
    else:
        if len(value.split(',')) == 1:
            term_values.append(value)
            term_join_check = True
            
        elif len(value.split(',')) == 5:
            track_year = int(value.split(',')[3])
            if track_year > max_track_year:
                max_track_year = track_year
            duration.append(float(value.split(',')[4]))
            track_join_check = True
                          
    current_key = key
    current_value = value


#Compute/output result for the last key
###
if track_join_check: 
    #compute/output result to STDOUT - track.artist_id, max(track.year), avg(track.duration),count(artist_term.term) 
    if term_join_check:
        term_count = sum([1 for i in term_values])*len(duration)
        print('{}\t{}'.format(current_key,(max_track_year,sum(duration)/len(duration),term_count)))
                          
    else:
        print('{}\t{}'.format(current_key,(max_track_year,sum(duration)/len(duration),0)))
                  
###