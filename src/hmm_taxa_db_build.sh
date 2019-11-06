#!/bin/bash
#read in MSAs
#hhbuild, then hhbuild -A for append


#1. #######Transform MAFFT clustal to clutal + stockholm format
#firstline
sed  -i '1i # STOCKHOLM 1.0' ./mafft_out/filename
sed -e -i  "\$a//" ./mafft_out/filename

#lastline
#sed -e "\$a//" filename > new_filename


#2. ######do the hmm build
FILES=$(ls ./mafft_out/*.fa) #change to $8

for f in $FILES; do
	extention=".hmm"
	newfil="$f${extention}"
	hmmbuild "${newfil}" $f;done


cat *.hmm > nucl_taxa_db

#hhcalibrate nucl_taxa_db
