# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 15:57:52 2019

@author: connorrp
"""


def get_seqs(tax_id):

    import os

    query = '"txid' + tax_id +\
         '[porgn] AND (refseq[filter] OR nuccore_genomes_samespecies[filter])"'

    out = tax_id+'.fasta'

    os.system('esearch -db nuccore -query ' + query +
              ' | efetch -db nuccore -format fasta > '+out)


if __name__ == "__main__":

    import sys

    inpt = str(sys.argv[1])

    get_seqs(inpt)
