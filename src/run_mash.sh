#!/bin/bash

#Create a sketch for contig file (fasta sequences)
#we use the seed value 0 because the refseq 88 database seed was 0. 
contig_file=$1
mash sketch -S 0 -i $contig_file
sketch_file=$1.msh
db_sketch_file=$2
dist_file=$3

#Run the mash dist program
mash dist $db_sketch_file $sketch_file -v 0.05 -p 8 > $dist_file

echo "done computing mash distances" 
