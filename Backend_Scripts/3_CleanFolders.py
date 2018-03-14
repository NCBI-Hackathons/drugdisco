import sys, os, subprocess, glob, path, shutil

# - Executable variables - #
srcdir="/nas02/home/m/c/mconvert/medusadockutils"
basedir="/lustre/scr/m/c/mconvert/test"
recedir="/nas02/home/m/c/mconvert/sod1"
rece="soddimer-opt.pdb"
orilig="bsdimer.mol2"
# ----------------------- #

# - Input variables - #
startdir=sys.argv[1]   # - initial folder to dock
enddir=sys.argv[2]     # - final folder to dock
# ----------------------- #


        # Operate recursively on the main folders, i.e., 001, 002, 003,...
        # according to the interval given as input

padding_len = len(startdir)

for i in xrange(int(startdir), int(enddir)+1):
    dir_format = '{:0' + str(padding_len) + '}'
    path=dir_format.format(i)
    #print path

        # Operate recursively on the main folders, i.e., 001, 002, 003,...
        # according to the interval given as input

    os.chdir(path)
    print os.getcwd()

    if os.path.exists('list.txt'):

                # Operate recursively on the subfolders, i.e., 001, 002, 003,...
                # according to what stored in list.txt

        with open('list.txt', "r") as f:
            line = f.readlines()
            for subdir in line:
                print subdir.rstrip()  
                os.chdir(str(subdir.rstrip()))
                for filename in glob.glob("*.min.mol2"):
                    del_dir = filename.replace(".min.mol2", "")
                    #print del_dir
                    if os.path.exists(del_dir):
                        shutil.rmtree(del_dir)

                os.chdir("../")

    os.chdir("../")

