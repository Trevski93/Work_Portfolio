#!/usr/bin/env python
import os
import sys


READING_artist_term = False
READING_track = False

if 'artist_term' in os.environ['mapreduce_map_input_file']:
    READING_artist_term = True
elif 'track' in os.environ['mapreduce_map_input_file']:
    READING_track = True
else:
    raise RuntimeError('Could not determine input file!')

# input comes from STDIN (standard input)
for record in sys.stdin:
    
    record = record.strip()
    data = record.split(',')
    
    if READING_artist_term:
        
        artist_id =  data[0]
        tag = data[1]
        print('{}\t{}'.format(artist_id,tag))
    
    else: 
        track_id = data[0] 
        title = data[1] 
        album = data[2] 
        year = data[3] 
        duration = data[4] 
        artist_id = data[5]
        print('{}\t{}'.format(artist_id,(track_id,title,album,year,duration)))
     
        
  