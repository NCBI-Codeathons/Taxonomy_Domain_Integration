"""
@author: KiranJavkar
Created on Tuesday, Nov 5th, 2019
"""

import numpy as np
import pandas as pd
from Bio import Phylo, SeqIO, Entrez, SeqRecord
import matplotlib
matplotlib.use('Agg')
from sklearn.decomposition import PCA
from collections import Counter
from sklearn.cluster import KMeans, DBSCAN
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import squareform, hamming
import math
import shlex, subprocess
import argparse, sys
from multiprocessing import Pool


def read_file(filepath):
    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()
    return lines


def write_file(filename, out_str):
    f = open(filename, 'w+')
    f.write(out_str)
    f.close()


def get_pricipal_components_count(model, min_explained_variance=0.8):
    cumsum = 0
    for idx, val in enumerate(model.explained_variance_ratio_):
        cumsum += val
        if(cumsum>=min_explained_variance):
            print(idx, cumsum)
            return idx
            break


def get_kmeans_elbow_point(dim_reduced_data, linearity_limiting_threshold=1.1):
    previous_slope = np.inf
    previous_sum_of_sq = np.inf
    k = 0
    while(True):
        k += 1
        print(k)
        km = KMeans(n_clusters=k)
        km = km.fit(X)
        current_sum_of_sq = km.inertia_
        if(k==1):
            previous_sum_of_sq = current_sum_of_sq
            continue
        else:
            current_slope = previous_sum_of_sq - current_sum_of_sq
            if(previous_slope <= linearity_limiting_threshold*current_slope):
                return k-2
            previous_slope = current_slope
            previous_sum_of_sq = current_sum_of_sq


def get_pricipal_components_count(model, min_explained_variance=0.8):
    cumsum = 0
    for idx, val in enumerate(model.explained_variance_ratio_):
        cumsum += val
        if(cumsum>=min_explained_variance):
            print(idx, cumsum)
            return idx
            break


def get_kmeans_elbow_point(X, linearity_limiting_threshold=1.1):
    previous_slope = np.inf
    previous_sum_of_sq = np.inf
    k = 0
    while(True):
        k += 1
#         print(k)
        km = KMeans(n_clusters=k)
        km = km.fit(X)
        current_sum_of_sq = km.inertia_
        if(k==1):
            previous_sum_of_sq = current_sum_of_sq
            continue
        else:
            current_slope = previous_sum_of_sq - current_sum_of_sq
            if(previous_slope <= linearity_limiting_threshold*current_slope):
                return k-2
            previous_slope = current_slope
            previous_sum_of_sq = current_sum_of_sq


def get_clustered_sequence_fasta(all_sequences_fasta_filename, cat_fasta_id_list, outfilename):
    cmd = "xargs samtools faidx {} < {} > {}".format(all_sequences_fasta_filename, cat_fasta_id_list, outfilename)
    print(cmd)
    try:
        p = subprocess.Popen(cmd, shell=True)
        # p = subprocess.Popen(shlex.split(cmd), shell=True)#, stdout=open(mum_results_file, 'w'))
        p.wait()
        print(cmd, ' output obtained')
    except Exception as e:
        print(cmd, e)


def get_clustered_sequences(similarity_matrix, sequence_names, all_sequences_fasta_filename,
                            out_dir, min_explained_variance=0.9, linearity_limiting_threshold=1.1):
    model_pca = PCA(n_components=similarity_matrix.shape[0])
    X = model_pca.fit_transform(similarity_matrix)
    n_principal_components = get_pricipal_components_count(model_pca, min_explained_variance)
    n_clusters = get_kmeans_elbow_point(X[:,:n_principal_components], linearity_limiting_threshold)
    print(n_clusters)
    kmeans_pca = KMeans(n_clusters=n_clusters)
    kmeans_pca = kmeans_pca.fit(X[:,:n_principal_components])
    print(Counter(kmeans_pca.labels_))
    pool = Pool(processes=8)
    for label in np.unique(kmeans_pca.labels_):
        opstr = ""
        temp_file = out_dir + "input_files_{}.txt".format(label)
        outfilename = out_dir + "input_files_{}.fasta".format(label)
        for name in sequence_names[kmeans_pca.labels_==label]:
            opstr += name.split()[0] + "\n"
        write_file(temp_file, opstr)
        pool.apply_async(get_clustered_sequence_fasta, args=(all_sequences_fasta_filename, temp_file, outfilename))
    pool.close()
    pool.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--distance_matrix', required=True, help="Input distance matrix file")
    parser.add_argument('-n', '--names', required=True, help="Sequence names")
    parser.add_argument('-s', '--all_sequence_fasta', required=True, help="All sequence fasta file")
    parser.add_argument('-o', '--out_dir', nargs='?', default='', help="Output directory for clustered fasta sequences")

    args = parser.parse_args()

    dist_mat = args.distance_matrix
    df = pd.read_csv(dist_mat, sep=' ', index_col=0)
    sequence_names = read_file(args.names)
    sequence_names = np.array([name.strip() for name in sequence_names])
    all_sequence_fastafile = args.all_sequence_fasta
    outdir = args.out_dir

    get_clustered_sequences(df.as_matrix(), sequence_names, all_sequence_fastafile, outdir)