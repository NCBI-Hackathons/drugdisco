<img src="https://github.com/NCBI-Hackathons/drugdisco/blob/master/DrugDiscoLogo.png" alt="DrugDisco Logo" width="200">

# DrugDisco
High throughput automated drug discovery: A pipeline to that tests over 20 million small molecules to find that one that fits your target  best!!!

## The problem
Developing new pharmaceutical drugs is crazy expensive. A big part of the cost comes from blindly screening millions of candidate compounds [cite]. 

## DrugDisco, the best fitting solution!

<img src="https://github.com/NCBI-Hackathons/drugdisco/blob/master/flowchart_overview.png" alt="DrugDisco Flowchart" width="1200">

DrugDisco works in two main stages. A back-end stage that downloads purchasable and drug-like compounds from the ZINC15 small-molecule database and clusters them and a front-end stage that attempts to find the compound that fits your target of choice best.

The back-end constsits of:

1. A script that checks ZINC15 every week and downloads all purchasable and drug-like compounds. Specifically, we download the ZINC-IDs and the SMILES and MOL2 representations of the small molecules. At the time of writing this document, there were over 20 million compounds that fit these categories.

2. We then calculate the Tanimoto similarities among all of the downloaded compounds.

3. Using the Tanimoto similarities, we cluster the compounds using [clustering method]. Compounds that are at least 95% similar are considered to be members of the same cluster.

4. Lastly, we store the clusters and choose the centroids of each cluster as the initial candidates for binding to target molecules.

## How to use DrugDisco

