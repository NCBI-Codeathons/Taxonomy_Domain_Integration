#!/bin/bash

Seqs=$1
DistOut=$2
NamesOut=$3
UserPATH=$4

TotalSeqs=`grep -c "^>" $Seqs`
NumIterations=$(($TotalSeqs * ($TotalSeqs - 1) / 2))


RScript $UserPATH/Taxonomy_Domain_Integration/src/PackageCheck.R

echo "Packages Present"

RScript $UserPATH/Taxonomy_Domain_Integration/src/RSingleRun.R $Seqs $DistOut $NamesOut

echo "Completed Synteny Maps"
