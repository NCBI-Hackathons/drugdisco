import sys, os, subprocess, glob, path, shutil

srcdir="/nas02/home/m/c/mconvert/medusadockutils"
basedir="/lustre/scr/m/c/mconvert/test"
recedir="/nas02/home/m/c/mconvert/sod1"
rece="soddimer-opt.pdb"
orilig="bsdimer.mol2"

startdir=sys.argv[1]
enddir=sys.argv[2]
padding_len = len(startdir)

for i in xrange(int(startdir), int(enddir)+1):
    dir_format = '{:0' + str(padding_len) + '}'
    path=dir_format.format(i)
    #print path
    os.chdir(path)
    print os.getcwd()

    if os.path.exists('list.txt'):
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

