# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:47:51 2019

@author: connorrp
"""

import pandas as pd
from itertools import product
from concurrent.futures import ThreadPoolExecutor
import multiprocessing


def joint_prob(args):

    m1 = args[0]
    m2 = args[1]
    name = args[2]

    t = list(m1.taxid.unique())
    d = list(m2.CDD.unique())

    df = pd.DataFrame(columns=['taxid', 'CDD', 'jp'])
    out = list()

    for i, pair in enumerate(product(d, t)):

        df.at[i, 'taxid'] = pair[1]
        df.at[i, 'CDD'] = pair[0]
        df.at[i, 'jp'] = (1 - m1[m1.taxid == pair[1]].distance.max())\
            * m2[m2.CDD == pair[0]].bitscore.max()

        if float(df.at[i, 'jp']) > 0:
            out.append([pair[1], pair[0], float(df.at[i, 'jp'])])

    df.to_csv(name+'_jp.tsv', '\t')

    return out


def cross_sum(args):

    jps = args[0]
    d = str(args[1])
    t = int(args[2])
    args[3]['CDD'] = d
    args[3]['taxid'] = t

    try:
        args[3]['score'] = sum(jps[t][d])/len(jps[t][d])
    except Exception:
        args[3]['score'] = 0


def dot_prod(m1, m2):

    print('\nLoading input data')
    t1 = pd.read_csv(m1, '\t', header=0)
    t2 = pd.read_csv(m2, '\t', header=0, index_col=0)
    t2.reset_index(inplace=True, drop=True)

    print('Normalizing primary key labels')
    t1['seq_id'] = t1['#sample_contig']
    t2['seq_id'] = t2.SRR+'_'+t2.contig_id

    print('Finding axis values')
    seq_ids = set(t1.seq_id.values).intersection(set(t2.seq_id.values))
    domains_ = set(t2.CDD.unique())
    taxa_ = set(t1.taxid.unique())
    print('There are ' + str(len(seq_ids)) +
          ' seq_ids, ' + str(len(domains_)) +
          ' domains, and ' + str(len(taxa_)) + ' taxa')

    print('Normalizing CDD bitscores')
    for x in t2.CDD.unique():

        for i in t2[(t2.CDD == x) & ~(t2.bitscore.isna())].index:
                t2.at[i, 'bitscore'] = t2.at[i, 'bitscore'].max()
                if t2.at[i, 'bitscore'] == 0:
                    raise ValueError('bitscore values should \
                                     be greater than 0')
        mxm = t2[(t2.CDD == x) & ~(t2.bitscore.isna())].bitscore.max()
        if (mxm > 0):
            for i in t2[t2.CDD == x].index:
                t2.at[i, 'bitscore'] = t2.at[i, 'bitscore'].max()/mxm
        else:
            print(x, mxm, t2[t2.CDD == x].bitscore.max())
    print('Normalization compelte')

    t2.to_csv('normd_domains.tsv', '\t')

    jps = dict()

    print('Calculating joint probabilities')
    cores = multiprocessing.cpu_count()-1
    with ThreadPoolExecutor(max_workers=cores) as executor:
        results = executor.map(joint_prob,
                               list([t1[t1.seq_id == idx],
                                     t2[t2.seq_id == idx], idx]
                                    for idx in seq_ids))
    print('Joint probabilities calculated')
    jps = dict()
    print('Indexing joint probabilities.')
    for result in list(item for sublist in results for item in sublist):
        try:
            jps[result[0]][result[1]].append(result[2])
        except Exception:
            try:
                jps[result[0]].update({result[1]: [result[2], ]})
            except Exception:
                jps.update({result[0]: {result[1]: [result[2], ]}})
    print('Index calculated')

    print('Dot product being calculated.')
    out = pd.DataFrame(index=[x for x in
                              range(len(list(product(domains_, taxa_))))],
                       columns=['taxid', 'CDD', 'score'])
    with ThreadPoolExecutor(max_workers=cores) as executor:
        executor.map(cross_sum, list([jps,
                                      pair[0],
                                      pair[1],
                                      out.loc[i, :]] for
                                     i, pair in
                                     enumerate(product(domains_, taxa_))))
    print('Dot product calculated. Writing output')

    out.to_csv('domains_v_taxonomy.tsv', '\t')
    out.dropna(inplace=True)
    out.to_csv('domains_v_taxonomy_cleaned.tsv', '\t')
    print('Done')


if __name__ == "__main__":

    import sys

    tax = str(sys.argv[1]).lstrip().rstrip()
    dom = str(sys.argv[2]).lstrip().rstrip()

    dot_prod(tax, dom)
