#!/usr/bin/env bash
# Usage: get_top_clusters.sh /path/to/zinc/library

mkdir top_clusters
mkdir top_clusters/smi
mkdir top_clusters/mol2

find_cluster_members.py -z $1

cd top_clusters/mol2
babel  ../smi/*.smi  *.mol2 -d