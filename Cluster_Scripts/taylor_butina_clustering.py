#!/usr/bin/env python

from __future__ import print_function

# An implementation of the Taylor-Butina clustering algorithm for
# chemical fingerprints.

# Modified from code by Andrew Dalke <dalke@dalkescientific.com>
# Distributed under the "MIT license"
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import sys
import argparse
import time
import numpy as np
import os

# I use the third-party "psutil" package to get memory use information.
try:
	import psutil
except ImportError:
	# If it isn't available, then don't report memory use.
	psutil = None
	def get_memory_use():
		return None
else:
	import os
	_process = psutil.Process(os.getpid())
	def get_memory_use():
		info = _process.memory_info()
		return info.rss # or info.vms?

# This requires chemfp. See http://chemfp.com/
import chemfp
from chemfp import search
		
# Convert the number of bytes into a more human-readable form.
def human_memory(n):
	if n < 1024:
		return "%d B" % (n,)
	for unit, denom in (("KB", 1024), ("MB", 1024**2),
						 ("GB", 1024**3), ("PB", 1024**4)):
		f = n/denom
		if f < 10.0:
			return "%.2f %s" % (f, unit)
		if f < 100.0:
			return "%d %s" % (round(f, 1), unit)
		if f < 1000.0:
			return "%d %s" % (round(f, 0), unit)
	return ">1TB ?!?"

##### Measure the current time and memory use, so I can generate a delta report.
class ProfileStats(object):
	def __init__(self, timestamp, memory_use):
		self.timestamp = timestamp
		self.memory_use = memory_use

def get_profile_stats():
	return ProfileStats(time.time(), get_memory_use())

def get_profile_time():
	return ProfileStats(time.time(), None)

def profile_report(title, start, end):
	dt = end.timestamp - start.timestamp
	if start.memory_use is None or end.memory_use is None:
		# Memory use not available.
		sys.stderr.write("%s time: %.1f sec\n" % (title, dt))
	else:
		delta_memory = end.memory_use - start.memory_use
		memory_str = human_memory(delta_memory)
		sys.stderr.write("%s time: %.1f sec memory: %s\n" % (title, dt, memory_str))

######

# The results of the Taylor-Butina clustering
class ClusterResults(object):
	def __init__(self, true_singletons, false_singletons, clusters):
		self.true_singletons = true_singletons
		self.false_singletons = false_singletons
		self.clusters = clusters

# The clustering implementation
def taylor_butina_cluster(similarity_table):
	# Sort the results so that fingerprints with more hits come
	# first. This is more likely to be a cluster centroid. Break ties
	# arbitrarily by the fingerprint id; since fingerprints are
	# ordered by the number of bits this likely makes larger
	# structures appear first.:

	# Reorder so the centroid with the most hits comes first.  (That's why I do
	# a reverse search.)  Ignore the arbitrariness of breaking ties by
	# fingerprint index

	centroid_table = sorted(((len(indices), i, indices)
								 for (i,indices) in enumerate(similarity_table.iter_indices())),
							reverse=True)

	# Apply the leader algorithm to determine the cluster centroids
	# and the singletons:

	# Determine the true/false singletons and the clusters
	true_singletons = []
	false_singletons = []
	clusters = []

	seen = set()
	for (size, fp_idx, members) in centroid_table:
		if fp_idx in seen:
			# Can't use a centroid which is already assigned
			continue
		seen.add(fp_idx)

		# Figure out which ones haven't yet been assigned
		unassigned = set(members) - seen

		if not unassigned:
			false_singletons.append(fp_idx)
			continue

		# this is a new cluster
		clusters.append( (fp_idx, unassigned) )
		seen.update(unassigned)

	# Return the results:
	return ClusterResults(true_singletons, false_singletons, clusters)

def report_cluster_results(cluster_results, arena, outfile):
	clusters = cluster_results.clusters

	# Sort so the cluster with the most compounds comes first,
	# then by alphabetically smallest id
	def cluster_sort_key(cluster):
		centroid_idx, members = cluster
		return -len(members), arena.ids[centroid_idx]

	clusters.sort(key=cluster_sort_key)

	clusters_dict = dict()
	cluster_size_dict = dict()
	centroids = []
	print(len(clusters), "clusters", file=outfile)
	for centroid_idx, members in clusters:
		clusters_dict[arena.ids[centroid_idx]] = [arena.ids[idx] for idx in members]
		centroids.append(arena.ids[centroid_idx])
		cluster_size_dict[arena.ids[centroid_idx]] = len(members)
	
	# print(clusters_dict) 
	np.save('cluster_dictionary.npy', clusters_dict)
	np.save('cluster_size_dictionary.npy', cluster_size_dict)

	# print(centroids)
	return centroids



#### Command-line driver

p = parser = argparse.ArgumentParser(
	description="An implementation of the Taylor-Butina clustering algorithm using chemfp")
p.add_argument("--threshold", "-t", type=float, default=0.8,
			   help="threshold similarity (default: 0.8)")
p.add_argument("--output", "-o", metavar="FILENAME",
			   help="output filename (default: stdout)")
p.add_argument("--profile", action="store_true",
			   help="report time and memory use")
p.add_argument("--version", action="version",
			   version="spam (using chemfp " + chemfp.__version__ + ")")
p.add_argument("fingerprint_filename", metavar="FILENAME")

# Turn the --output option into a file object and close function.
def _close_nothing():
	pass

def open_output(parser, filename):
	## open a file, or use None to use stdout
	if filename is None:
		return sys.stdout, _close_nothing
	try:
		outfile = open(filename, "w")
	except IOError as err:
		parser.error("Cannot open --output file: %s" % (err,))
	return outfile, outfile.close

## 

def main(args=None):
	args = parser.parse_args(args)

	if args.profile and psutil is None:
		sys.stderr.write("WARNING: Must install the 'psutil' module to see memory statistics.\n")

	# Load the fingerprints
	start_stats = get_profile_stats()
	try:
		arena = chemfp.load_fingerprints(args.fingerprint_filename)
	except IOError as err:
		sys.stderr.write("Cannot open fingerprint file: %s" % (err,))
		raise SystemExit(2)

	# Make sure I can generate output before doing the heavy calculations
	outfile, outfile_close = open_output(parser, args.output)

	try:
		load_stats = get_profile_stats()

		# Generate the NxN similarity matrix for the given threshold
		similarity_table = search.threshold_tanimoto_search_symmetric(
			arena, threshold = args.threshold)
		similarity_stats = get_profile_stats()

		# Do the clustering
		cluster_results = taylor_butina_cluster(similarity_table)
		cluster_stats = get_profile_stats()

		# Report the results
		centroids = report_cluster_results(cluster_results, arena, outfile)

		#########
		#This is the list of zinc ids in the cluster
		#########
		
		fh = open('HDAA.smi', "r")
		n = 0
		for line in fh:
			id  = line.split()[1] 
			if id in centroids:
				centroid_file = open("centroids/smi/" + id + ".smi", "w")
				centroid_file.write(line)
				n = n + 1
				centroid_file.close()
		print("\nNumber of centroids: " + str(n) + "\n")
		fh.close()
		

		# Report the time and memory use.
		if args.profile:
			print("#fingerprints:", len(arena), "#bits/fp:", arena.num_bits, "threshold:", args.threshold,
				  "#matches:", similarity_table.count_all(), file=sys.stderr)
			profile_report("Load", start_stats, load_stats)
			profile_report("Similarity", load_stats, similarity_stats)
			profile_report("Clustering", similarity_stats, cluster_stats)
			profile_report("Total", start_stats, get_profile_time())
	finally:
		outfile_close()

if __name__ == "__main__":
	main()
