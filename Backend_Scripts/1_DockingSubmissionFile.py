import sys,os,subprocess,glob

srcdir='/nas02/home/m/c/mconvert/medusadockutils'
basedir='/lustre/scr/m/c/mconvert/test'
recedir='/nas02/home/m/c/mconvert/sod1'
rece='soddimer-opt.pdb'
orilig='bsdimer.mol2'

# - Input variables - #
# - initial folder to dock
start_dir=sys.argv[1]
# - final folder to dock
end_dir=sys.argv[2]
# - number of ligands to dock
num_lig=int(sys.argv[3])
# - number of docking
num_dock=int(sys.argv[4])
# queue for HPC
queue=sys.argv[5]
padding_len = len(start_dir)

def save_makedir(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

for i in xrange(int(start_dir), int(end_dir)+1):
	dir_format = '{:0' + str(padding_len) + '}'
	#print(dir_format)
	cdir=dir_format.format(i)
	os.chdir(str(cdir))
	# Split in Dirs
	# This portion of the script will generate a series of subfolders (i.e., 001, 002,...) within the main folder.
	# Each subfolder will contain a number of molecules equal to what specified in numlig variable 
	onlyfiles = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f))]	
	subdir_num = 1
	for cnt, file in enumerate(onlyfiles):
		if cnt % num_lig == 0:
			sub_dir=dir_format.format(subdir_num)
			save_makedir(sub_dir)
			sub_dir_path = os.path.abspath(sub_dir)
			#print(sub_dir_path)
			subdir_num+=1
		os.rename(os.path.join('.', file), os.path.join(sub_dir_path, file))
	
	onlydirs = [x[0][2:] for x in os.walk('.') if x[0] != '.']
	#construct list.txt	
	with open( 'list.txt', 'w' ) as f:
		for d in onlydirs:
			f.write(d+'\n')
			
	#construct sub.sh file
	for d in onlydirs:
		with open( os.path.join(d, 'sub.sh'), 'w' ) as f:
			f.write('#!/bin/bash'+'\n')
			f.write('#SBATCH --job-name=c001-001'+'\n')
			f.write('#SBATCH --time=200:00:00'+'\n')
			f.write('#SBATCH -o output_%j.out # File to which STDOUT will be written'+'\n')
			f.write('#SBATCH -e error_%j.err # File to which STDERR will be written'+'\n')
			f.write('cd {}\n'.format(basedir))
			f.write('sh {}\n'.format(os.path.join(basedir, d, 'dock.sh')))
	
	#construct  dock.sh file 
	for d in onlydirs:
		with open( os.path.join(d, 'dock.sh'), 'w' ) as f:
			f.write('#!/bin/bash'+'\n')
			f.write('for i in *.min.mol2'+'\n')
			f.write('do'+'\n')
			f.write('dir_name=$(echo $i | awk -F".min.mol2" \'{print $1}\')'+'\n')
			f.write('mkdir $dir_name'+'\n')
			f.write('for c in $(seq -w 1 10)' +'\n')
			f.write('do'+'\n')
			f.write('rng=$RANDOM'+'\n')
			f.write('a=${i/mol2/pdb}'+'\n')
			exe_name = os.path.join(srcdir, 'medusaDock.linux')
			rec_name = os.path.join(recedir, rece)
			param_name = os.path.join(srcdir, 'Medusa-Param/')
			rec_loc_name = os.path.join(recedir, orilig)
			f.write('{} -i {} -m ${{i}} -o $dir_name/$c.$rng.pdb -p {} -M {} -r 12 -R -S $rng'.format(exe_name, rec_name, param_name, rec_loc_name) + '\n')
			f.write('done'+'\n')
			f.write('done'+'\n')


	os.chdir('../')

