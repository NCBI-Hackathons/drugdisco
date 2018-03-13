<img src="https://github.com/NCBI-Hackathons/drugdisco/blob/master/DrugDiscoLogo.png" alt="DrugDisco Logo" width="200">

# DrugDisco
DrugDisco is a high throughput automated drug discovery tool. Specifically, it tests over 20 million small molecules that are commercially available and can be used a drugs to find that one that fits your target best!!!

DrugDisco is for anyond interested in rational and structure-based drug discovery. Why test compounds at random when DrugDisco will sort through them for you?

## The problem
Developing new pharmaceutical drugs is crazy expensive. A big part of the cost comes from blindly screening millions of candidate compounds [cite]. Ultimately, trying each one out in cell cultures or animals is too time consuming, too costly and ethically unsound.

## DrugDisco, the best fitting solution!
DrugDisco makes trial-and-error drug discovery a thing of the past by using a rational and structure-based approach. It can screen millions of compounds in-silico to find the best fiting ligand for your target.

## How it works:
DrugDisco consists of 3 main components:

1. A "back-end" or "database" component that stores relavant information about the ligands and how similar they are to each other.
2. A user-interface that lets you specify a target molecule 
3. A "filtering" component that identifies the compound that best fits your target of choice.

<img src="https://github.com/NCBI-Hackathons/drugdisco/blob/master/flowchart_overview.png" alt="DrugDisco Flowchart" width="1200">

The back-end constsits of:

1. A script that checks ZINC15 every week and downloads all purchasable and drug-like compounds. Specifically, we download the ZINC-IDs and the SMILES and MOL2 representations of the small molecules. At the time of writing this document, there were over 20 million compounds that fit these categories.

2. We then calculate the Tanimoto similarities among all of the downloaded compounds.

3. Using the Tanimoto similarities, we cluster the compounds using [clustering method]. Compounds that are at least 95% similar are considered to be members of the same cluster.

4. Lastly, we store the clusters and choose the centroids of each cluster as the initial candidates for binding to target molecules.

The user interface allows users to upload a target molecule in PDB format, a binding site in MOL2 format providing the x, y and z coordinates for the center of the binding site and their email address so that they can be notified when DrugDisco has idientified 20 candidate compounds.

The filtering component progressively refines its search by using MedusaDock on the target molecule and candidate compounds:

1. In the first round, MedusaDock runs for 10 iterations using the target molecule and every compound that was identified as a cluster centroid. The top 1,000 compounds are then selected for the second round.

2. In the second round, MeduaDock runs for 250 iterations using the top 1,000 compounds identified in the previous step. The top 100 compounds are then selected for the third round.

3. In the third round, MedusaDock runs for 1,000 iterations using the top 100 compounds from the previous step. The top 20 compounds are then selected for the fourth round.

4. In the fourth round, all of the compounds in the clusters represented by the top 20 compounds identified in the previous step are run through steps 1, 2 and 3. The final top 20 compounds, their ZINC-ID and their final scores, ranked from best to worst, are returned to the user.

## How to use DrugDisco, a step-by-step tutorial
This is where we add screenshots that show exactly, step-by-step, how to use DrugDisco.

