from __future__ import print_function
import os
import numpy as np
import sys
import random
import glob

data_dir=sys.argv[1]
output_script_dir = 'out_scripts'
output_data_dir = 'out_data'
output_topN = 20

parallel_num = int(sys.argv[2])
docking_times =int(sys.argv[3])
csvFile_name = sys.argv[4]

def save_makedir(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)
	
rece='soddimer-opt.pdb'
orilig='bsdimer.mol2'	

mol_files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f)) and f.endswith('mol2')]	
num_mols = len(mol_files)
print(num_mols)
group_size = int(np.floor(num_mols / parallel_num))

#exe_name = os.path.join('', 'medusaDock.linux')
exe_name = os.path.join("", 'dummy_dock.py')
rec_name = os.path.join('', rece)
param_name = os.path.join('', 'Medusa-Param/')
rec_loc_name = os.path.join('', orilig)

save_makedir(output_script_dir)
padding_len = 3

for g in xrange(parallel_num):
	with open( os.path.join(output_script_dir, 'sub_grp{}.sh'.format(g)), 'w' ) as f:
		f.write('#!/bin/bash'+'\n')
		f.write('#SBATCH --job-name=c001-001'+'\n')
		f.write('#SBATCH --time=200:00:00'+'\n')
		f.write('#SBATCH -o output_%j.out # File to which STDOUT will be written'+'\n')
		f.write('#SBATCH -e error_%j.err # File to which STDERR will be written'+'\n')
		f.write('sh {}\n'.format('dock_grp{}.sh'.format(g)))
	with open( os.path.join(output_script_dir, 'dock_grp{}.sh'.format(g)), 'w' ) as f:
		end_idx = (g+1)*group_size
		if g == parallel_num-1:
			end_idx = num_mols
		c_mol_files = mol_files[g*group_size:end_idx]
		for file in c_mol_files:
			out_path_prefix = os.path.join( output_data_dir, file[:-5] )
			for time in xrange(docking_times):
				out_path = os.path.join(out_path_prefix, '{}_{:03}.pdb'.format(file[:-5], time))
				if 'dummy' in exe_name:
					f.write('python {} -i {} -m {} -o {} -p {} -M {} -r 12 -R -S {}'.format(exe_name, rec_name, file, out_path, param_name, rec_loc_name, random.randint(0, 32767)) + '\n')
				else:
					f.write('{} -i {} -m {} -o {} -p {} -M {} -r 12 -R -S {}'.format(exe_name, rec_name, file, out_path, param_name, rec_loc_name, random.randint(0, 32767)) + '\n')
					
#docking...
if 'dummy' in exe_name:
	for g in xrange(parallel_num):
		print('starting group {}... ...'.format(g), end='')
		script_path = os.path.join(output_script_dir, 'dock_grp{}.sh'.format(g))
		os.system('sh '+ script_path)
		print('finishing group {}'.format(g))
else:
	for g in xrange(parallel_num):
		script_path = os.path.join(output_script_dir, 'sub_grp{}.sh'.format(g))
		os.system('sh '+ script_path)
		
outdir='./out_data'
#outdir='./output'


csvFile = open(csvFile_name, "w")
csvFile.write("Compounds,MIN_E,SUB_ZINC_ID,POSE\n")

os.chdir(outdir)
# read all dir name
onlydirs = [f for f in os.listdir('.') if os.path.isdir(os.path.join('.', f))]
csv_fields = [] 

for dname in onlydirs:
    #print dname
    os.chdir(dname)
    csv_line = []
    for filename in glob.glob("*.pdb"):
        #print filename[:-4]
        min_pose = -1
        min_eng = 0
        with open(filename, "r") as f:
            lines = f.readlines()
	    tmp_pose = -1
        for line in lines:
            if line.startswith('REMARK POSE'):
                tmp_pose = int(line[13:].rstrip())
                #print tmp_pose
            if line.startswith('REMARK E_total'):
                if min_eng > float(line[16:].rstrip()):
                    min_pose = tmp_pose
                    min_eng = float(line[16:].rstrip())
                #print "P[" + str(min_pose) + "]; Min E: " + str(min_eng)
	    csv_line = dname + "," + str(min_eng) + "," + filename[:-4] + "," + str(min_pose) + "\n"
    csv_fields.append((dname, min_eng, filename[:-4], min_pose))      #print csv_line
    

    os.chdir("../")

os.chdir("../")

csv_fields.sort(key=lambda x: x[1])
for cnt, ff in enumerate(csv_fields):
	csv_line = ff[0] + "," + str(ff[1]) + "," + ff[2] + "," + str(ff[3]) + "\n"
	csvFile.write(csv_line)
	if cnt >= output_topN-1:
		break


csvFile.close()

os.system('rm -rf out_scripts')
os.system('rm -rf out_data')
