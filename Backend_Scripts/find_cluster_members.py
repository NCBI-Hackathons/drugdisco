#!/usr/bin/env python
from __future__ import print_function
import pandas as pd
import numpy as np
import argparse


p = parser = argparse.ArgumentParser(
	description="Find all members of the clusters to which a list of centroids belongs")
p.add_argument("--zinc_path", "-z", type=str,
			   help="path to directory containing zinc_library.smi file")

def main(args=None):

	args = parser.parse_args(args)
	zinc_path = args.zinc_path
	# zinc_path = args[0]

	df = pd.read_csv("energies.csv")
	centroids = df.Compounds #you can also use df['column_name']

	# print(centroids)

	clus_dict = np.load(zinc_path + '/cluster_dictionary.npy').item()

	# print(clus_dict)
	# print(clus_dict['ZINC000049401119'])
	clus_mem = []
	for cmpd in centroids:
		# print(centroids)
		clus_mem.append(clus_dict[cmpd])

	clus_mem = [y for x in clus_mem for y in x]

	fh = open(zinc_path + '/zinc_library.smi', "r")
	n = 0
	for line in fh:
		id  = line.split()[1] 
		if id in clus_mem:
			centroid_file = open("top_clusters/smi/" + id + ".smi", "w")
			centroid_file.write(line)
			n = n + 1
			centroid_file.close()
	print("\nNumber of cluster members: " + str(n) + "\n")
	fh.close()

# main()

if __name__ == "__main__":
	main()