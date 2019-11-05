import os
import sys

with open(sys.argv[1]) as f:
	for num,line in enumerate(f):
		if line.startswith('accession'):
			continue
		val = line.strip().split(',')
		print (val)
		command1 = "gsutil cat gs://ncbi_sra_realign/contigs/" + str(val[0]) + ".contigs.fasta > temp.fasta"
		command0 = "samtools faidx temp.fasta"
		command2 = "samtools faidx temp.fasta "+ str(val[1]) + " >> sequences.fasta"
		# if num >= 5:
		# 	break
		try:
		  os.system(command1)
		  os.system(command0)
		  os.system(command2)
		  os.system("rm temp.fasta*")

		except:
		  print("command does not work")

		