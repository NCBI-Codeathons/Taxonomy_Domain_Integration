import os
import sys
import argparse

def main():
	parser = argparse.ArgumentParser(description="Outputs taxa assignment based on filtering of mash distances")
	parser.add_argument("-m","--refseq_map", help="Refseq genome assembly to taxid mapping (refseq_genome_info.csv)",required=True)
	parser.add_argument("-d","--contig_dist_file", help="Mash distance file for mapping query sequences (contigs) to refseq sketch",required=True)
	parser.add_argument("-o","--output_file", help="query sequence to taxid to distance tuple (sparse representation of query sequence to taxid matrix) (csv file format) ")

	args = parser.parse_args()

	acc2taxid = {}
	file2taxid = {}
	acc2taxidspecies = {}
	file2taxidspecies = {}
	with open (args.refseq_map) as f:
		for num, line in enumerate(f):
			if num == 0:
				continue
			val = line.strip().split(',')
			filefinal = val[0].split('.gz')[0]
			acc2taxid[val[1]]= val[2]
			acc2taxidspecies[val[1]] = val[3]
			file2taxid[filefinal] = val[2]
			file2taxidspecies[filefinal] = val[3]


	#TODO Can incorporate shared hash functions in the future
	fw = open(args.output_file, "w")
	fw.write("#queryseq,taxid,speciestaxid,distance\n")
	distance_threshold = 1
	with open (args.contig_dist_file) as f:
		for line in f:
			val = line.strip().split('\t')
			if float(val[2]) <= distance_threshold:
				key = val[0].split('.gz')[0]
				taxa = "NA"
				speciestaxa = "NA"
				if key in file2taxid:
					taxa = file2taxid[key]
					speciestaxa = file2taxidspecies[key]
				# else:
				# 	accname = val[0].split('_A')[0]
				# 	taxa = acc2taxid[accname]
				# 	speciestaxa = acc2taxidspecies[accname]
				fw.write(','.join([val[1], str(val[0]), str(taxa), str(speciestaxa),str(val[2])])+'\n')
				
	fw.close()
if __name__ == '__main__':
	main()