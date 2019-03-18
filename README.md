# Work_Portfolio

This is a repository that contains some of the projects I've worked on.
Included here: 
1. Script written for the Travelling salesman problem
2. folders "groups","joins", and "matmul" inlucde map reduce algorithms I've written to perform the following (actual mapper and reducers are located in the "src" folders within each main folder): 
  1. groups : SQL query equivalent -> SELECT 	artist_id, track_id, term FROM	track INNER JOIN artist_term ON track.artist_id = artist_term.artist_id
  2. joins : SQL query equivalent -> SELECT track.artist_id, max(track.year), avg(track.duration), count(artist_term.term) FROM track LEFT JOIN artist_term ON track.artist_id = artist_term.artist_id GROUP BY track.artist_id
  3. matmul : matrix multiplication 
