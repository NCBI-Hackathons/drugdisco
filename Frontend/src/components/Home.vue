<template>
<div class="introduction">
  <h3>MedusaDock</h3>
  <p>Existing flexible docking approaches model the ligand and receptor flexibility either separately or in a loosely
  coupled manner, which captures the conformational changes inefficiently. Here, we propose a flexible docking
  approach, MedusaDock, which models both ligand and receptor flexibility simultaneously with sets of discrete
  rotamers. We developed an algorithm to build the ligand rotamer library "on-the-fly" during docking
  simulations. MedusaDock benchmarks demonstrate a rapid sampling efficiency and high prediction accuracy
  in both self- (to the cocrystallized state) and cross-docking (to a state cocrystallized with a different ligand),
  the latter of which mimics the virtual screening procedure in computational drug discovery. We also perform
  a virtual screening test of four flexible kinase targets, including cyclin-dependent kinase 2, vascular endothelial
  growth factor receptor 2, HIV reverse transcriptase, and HIV protease. We find significant improvements of
  virtual screening enrichments when compared to rigid-receptor methods. The predictive power of MedusaDock
  in cross-docking and preliminary virtual-screening benchmarks highlights the importance to model both
  ligand and receptor flexibility simultaneously in computational docking.</p>
  <img src="static/schema.png" />
  <p><i>Figure. Schema for the MedusaDock protocol. Each docking simulation starts with the generation of the STROLL, followed by
    the clustering of ligand rotamers (Methods) with a kRMSD cutoff of 2 &Aring;. The NC cluster centroids are used as the 
    representative ligand conformations for the initial coarse-docking, where the ligand is kept rigid and the ligand binding 
    pocket is rapidly sampled (Methods). Since only a small number of the ligand rotamers is used and the ligand is kept rigid 
    during coarse-docking, the nearnative pose is not necessarily the lowest energy pose but usually is among the low-energy 
    poses. We sort the NC poses according to binding energies. We group similar poses together if the RMSD of two ligand poses
    is smaller than their kRMSD plus 2 &Aring;. The grouping of similar poses will reduce the necessary number of the more
    expensive calculations of fine docking. We select the top NF (~10% NC) groups of lowest energy poses for the next round of
    fine docking. For each group of coarse-docked poses, we perform fine docking to enrich the ligand rotamers and to minimize
    the total energy (Methods). During fine docking, we add the ligand rotamers within 2.0 &Aring; kRMSD to the initial centroid
    rotamer in order to enrich the ligand conformation. For each of the members in a group, we perform the enrichment step. We
    only select the lowest energy poses for further minimization (Methods). Therefore, we will have NF poses for each MedusaDock
    run.</i></p>
  <h4>Reference</h4>
  <ol>
    <li>Ding, F., Yin, S., & Dokholyan, N. V. (2010). Rapid flexible docking using a stochastic rotamer library of ligands. Journal of Chemical Information and Modeling, 50(9), 1623-1632.</li>
    <li>Yin, S., Biedermannova, L., Vondrasek, J., & Dokholyan, N. V. (2008). MedusaScore: An accurate force field-based scoring function for virtual drug screening. Journal of Chemical Information and Modeling, 48(8), 1656-1662.</li>
  </ol>
</div>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
    }
  },
  methods: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.introduction {
  padding: 10px 30px;
}

</style>
