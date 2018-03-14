<img src="https://github.com/NCBI-Hackathons/drugdisco/blob/master/DrugDiscoLogo.png" alt="DrugDisco Logo" width="200">

# DrugDisco
DrugDisco is a high throughput automated drug discovery pipeline. Specifically, it tests over 20 million small molecules that are commercially available and can be used a drugs to find that one that fits your target best!!!

DrugDisco is for anyone interested in rational and structure-based drug discovery. Why test compounds at random when DrugDisco will sort through them for you?

## The problem
Developing new pharmaceutical drugs is crazy expensive. A big part of the cost comes from blindly screening millions of candidate compounds [cite]. Ultimately, trying each one out in cell cultures or animals is too time consuming, too costly and ethically unsound.

## DrugDisco, the best fitting solution!
DrugDisco makes trial-and-error drug discovery a thing of the past by using a rational and structure-based approach. It can screen millions of compounds _in silico_ to find the best fitting ligand for your target. It does this by combining the commercial, drug-like compounds in the ZINC15 database with the protein docking program of your choice.

In the picture below, the big blue blob is a target molecule and the red dot marks the spot where we want to fit a ligand. DrugDisco will sort through 20 million ligands and find the one that's most snug.
<img src="https://github.com/NCBI-Hackathons/drugdisco/blob/master/dock-example.png" alt="molecule with binding site" width="600">


## How it works:
DrugDisco consists of 3 main components:

1. A **back-end** or **database component** that stores relevant information about the ligands and how similar they are to each other.
2. A **user-interface** that lets you specify a target molecule 
3. A **filtering component** that identifies the compound that best fits your target of choice.

<img src="https://github.com/NCBI-Hackathons/drugdisco/blob/master/figure1.png" alt="DrugDisco Flowchart" width="1200">

The **back-end/database component** constsits of:

1. A script that downloads all purchasable and drug-like compounds from ZINC15. Specifically, DrugDisco downloads the ZINC-IDs and the SMILES and MOL2 representations of the small molecules. At the time of writing this document, there were over 20 million compounds that fit these categories.

2. DrugDisco then calculates the Tanimoto similarities among all of the downloaded compounds [cite].

3. Using the Tanimoto similarities, DrugDisco clusters the compounds using Taylor-Butina clustering [cite]. Compounds that are at least 95% similar are considered to be members of the same cluster.

4. Lastly, DrugDisco store the clusters in a file containing each ZINC-ID and the cluster number that that molecule is associated with. DrugDisco selects centroids of each cluster as the initial candidates for binding to target molecules.

The **user interface** allows users to upload a target molecule in PDB format, a binding site in MOL2 format providing the x, y and z coordinates for the center of the binding site and their email address so that they can be notified when DrugDisco has identified 20 candidate compounds.

The **filtering component** progressively refines its search by using a docking program on the target molecule and candidate compounds. We have provided scripts that allow DrugDisco to work with X, Y and Z docking programs. However, if you would like to use an alternative docking program, you can write a wrapper script that take a target molecule in PDB format, a binding site in MOL2 format and a ligand in MOL2 format as input.

Here are the steps for filtering:

1. In the first round, the docking program runs for 10 iterations using the target molecule and every compound that was identified as a cluster centroid. The top 1,000 compounds are then selected for the second round.

2. In the second round, the docking program runs for 250 iterations using the top 1,000 compounds identified in the previous step. The top 100 compounds are then selected for the third round.

3. In the third round, the docking program runs for 1,000 iterations using the top 100 compounds from the previous step. The top 20 compounds are then selected for the fourth round.

4. In the fourth round, all of the compounds in the clusters represented by the top 20 compounds identified in the previous step are run through steps 1, 2 and 3. The final top 20 compounds, their ZINC-ID and their final scores, ranked from best to worst, are emailed to the user.

Here is an overview of how the three major components come together using computer hardware:
<img src="https://github.com/NCBI-Hackathons/drugdisco/blob/master/platform_overview.png" alt="Platform Flowchart" width="1200">

## How to use DrugDisco, a step-by-step tutorial
<img src="https://github.com/NCBI-Hackathons/drugdisco/blob/master/web4.PNG" alt="DrugDisco UI" width="1200">

* Step 1: Next to **Receptor** click on "Choose File" and select your PDB formated target molecule.
* Step 2: Next to **Binding Coordinates** click on "Choose File" and select your MOL2 formatted x, y, z binding coordinates.
* Step 3: Enter your email address
* Step 4: Press "Submit"

# BAM!!!!!
