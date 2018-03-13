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

The front-end consists of a user interface along with a series of steps that progressively refine the search for the best fitting compound.

1. The users provides a target molecule by entering a PDBID. DrugDisco then downloads the 3-D structure of this molecule from PDB and renders it in the browser. If there is no 3-D structure for the molecule of iterest, it can be uploaded by the user.

2. The user then specifies the center of the binding site by clicking on the 3-D rendered molecule or by entering it by hand.

3. Lastly the user enters their email address so that they can be notified when DrugDisco has idientified 20 candidate compounds.

3. DrugDisco then progressively refines its search by using MedusaDock on the target molecule and candidate compounds. 
  1. In the first round, MedusaDock runs for 10 iterations using the target molecule and every compound that was identified as a cluster centroid. The top 1,000 compounds are then selected for the second round.
  2. In the second round, MeduaDock runs for 250 iterations using the top 1,000 compounds identified in the previous step. The top 100 compounds are then selected for the third round.
  3. In the third round, MedusaDock runs for 1,000 iterations using the top 100 compounds from the previous step. The top 20 compounds are then selected for the fourth round.
  4. In the fourth round, all of the compounds in the clusters represented by the top 20 compounds identified in the previous step are run through steps 1, 2 and 3. The final top 20 compounds, their ZINC-ID and their final scores, ranked from best to worst, are returned to the user.

## How to use DrugDisco

