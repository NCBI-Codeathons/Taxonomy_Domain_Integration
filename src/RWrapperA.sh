#!/bin/bash

# import a fasta file into R
# convert seqs into a sqlite database for DECIPHER
# generate synteny maps in parallel
# approximate a jaccard distance from synteny maps
# collapse parallelized distances into a single distance matrix
# output a distance matrix
# output a txt of unique names
# output an RData file for redundancy

# Necessary to force R to use the correct installation
# export PATH=/opt/anaconda2/bin:$PATH
# Path for testing locally
# export PATH=~/Dropbox/CodeAthons/TDILocal/src:$PATH
# Path for running out of the box on the VM
# export PATH=~/Taxonomy_Domain_Integration/src:$PATH

TempDir01=$(mktemp -d) # tempdir for R Objects
TempDir02=$(mktemp -d) # tempdir for Queue Objects
TempDir02=$(mktemp -d) # tempdir for MSA

Seqs=$1
DistOut=$2
NamesOut=$3
UserPATH=$4

TotalSeqs=`grep -c "^>" $Seqs`

NumIterations=$(($TotalSeqs * ($TotalSeqs - 1) / 2))

# RScript ~/Dropbox/CodeAthons/TDILocal/src/PackageCheck.R
RScript $UserPATH/Taxonomy_Domain_Integration/src/PackageCheck.R

echo "Packages Present"

# RScript ~/Dropbox/CodeAthons/TDILocal/src/ScriptA.R $Seqs $TempDir01
RScript $UserPATH/Taxonomy_Domain_Integration/src/RScriptA.R $Seqs $TempDir01

echo "Initial Data completed"


# This step needs to be parallelized
for val in `seq $NumIterations`
do
  # (RScript ~/Dropbox/CodeAthons/TDILocal/src/ScriptB.R $val $SqlFile $QueueFolder $RDataInitial || echo failed >$QueueFolder.$val.err) &
  # RScript ~/Dropbox/CodeAthons/TDILocal/src/ScriptB.R $val $TempDir01 $TempDir02
  RScript $UserPATH/Taxonomy_Domain_Integration/src/RScriptB.R $val $TempDir01 $TempDir02
done
# wait

echo "Loop Completed"

# RScript ~/Dropbox/CodeAthons/TDILocal/src/ScriptC.R $TempDir01 $TempDir02 $DistOut $NamesOut
RScript $UserPATH/Taxonomy_Domain_Integration/src/RScriptC.R $TempDir01 $TempDir02 $DistOut $NamesOut

echo "R Section Completed"


