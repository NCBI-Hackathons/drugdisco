#!/usr/bin/env bash

# This script assumes that you have already downloaded the curl from zinc for the smi files of your choice
# It was not clear how to use the ZINC api to generate this file
# Save the curl in a directory where you would like to keep your zinc library
csh ZINC-downloader-2D-smi.curl

#remove the headers from the smiles file
for f in *.smi; do
    tail -n +2 "$f" > "${f}".tmp && mv "${f}".tmp "$f"
    echo "Processing $f"
done

cat *.smi > zinc_library
rm *.smi
mv zinc_library zinc_library.smi



mkdir centroids
mkdir centroids/smi
mkdir centroids/mol2

# Generating fingerprints for smiles file
# Babel FP2 fingerprints used currently (path based, min = 1, max = 7, 1024 bits)
# took 5 minutes with 50,000 cmpds
# rename smiles file!
rdkit2fps zinc_library.smi --fpSize 1024 > zinc_library.fps

# performs talyor butina clustering, outputs mol2 files for the centroid
# reports performance measures take about 1 minutes with 50,000 compounds with 1 gb of memory
taylor_butina_clustering.py --profile --threshold 0.95 zinc_library.fps -o zinc_library.centroids
cd centroids/mol2
babel  ../smi/*.smi  *.mol2 -d

