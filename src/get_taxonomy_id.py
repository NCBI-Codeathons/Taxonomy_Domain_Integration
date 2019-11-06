import os
import sys

taxid = {}
taxname = {}

with open(sys.argv[1]) as f:
	for line in f:
		val = line.strip().split('\t')
		valarr = [x for x in val[1].split(' ') if x!='']
		tid = val[1].split(' ')[0]
		taxid[val[0]] = tid
		name = ' '.join(valarr[2:])
		taxname[tid] = name
		

fs = open('taxonomy_3k.tsv', 'w')
fs.write('#sample_contig\tref_seq_accession\ttaxid\ttax_name\tdistance\tpvalue\tshared_hashes\ttotal_hashes\n')
with open (sys.argv[2]) as f:
	for line in f:
		filename = line.strip()
		# print (filename)
		# filename = "3k/SRR953964.realign.local.fa.dist"
		fileid = filename.split('/')[-1].split('.')[0]
		with open (filename) as fw:
			# print ("hellp")
			for linefw in fw:
				# print ("hello")
				val = linefw.strip().split('\t')
				# print val
				taxidkey = taxid[val[0]]
				key = fileid + '_' + val[1]
				printarr = [key, val[0], taxidkey, taxname[taxidkey],val[2], val[3], val[4], val[5]]
				fs.write('\t'.join(printarr) + '\n')
				# print val, key, taxidkey
				

		
fs.close()

