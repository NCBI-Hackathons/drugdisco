#!/usr/bin/env bash
# Usage: docking_pipeline.sh path/to/zinc/library
# Run this in a directory for your docking run

# First run of the docking pipeline, generates
# energies.csv file with the top ranked ligands
# and their binding energies

python automatic_screening.py centroid_min 10 5 energies_stage1.csv 
# Get the other cluster members of the top
# ranked ligands

get_top_clusters.sh $1 

# Rerun docking with all cluster members
# located in ./top_clusters/mol2

python automatic_screening.py top_clusters/mol2 10 5 energies_stage2.csv
