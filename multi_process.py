import os
import shutil
import glob
import random
import multiprocessing as mp
import sys
import fileinput
import subprocess as sub
import numpy as np
import math
import pdb

# --------------------------------------------------------------------

def get_VSPACE(input_file,project_dir):
    destList = []
    os.chdir(project_dir)
    vsl = open(input_file, 'r')
    for line in vsl:
        project_dir= vsl.readlines()[0]
        line.strip().split('/n')
        vspace_name = line.split()
        vsf = open(vspace_name, 'r+')
        vspace_all = vsf.readlines()
        check = vspace_all[3]
        destLine = vspace_all[1]
        destfolder = project_dir + destLine.strip().split(None, 1)[1]
        destList.append(destfolder)
        if "samplemode" in check:
            os.system('vspace ' + vspace_name)
            rand_dist(destfolder, vspace_name)
        else:
            os.system('vspace ' + vspace_name)
    return destList

# --------------------------------------------------------------------

def rand_dist(folder_name, vspace_file):
    vspace = open(vspace_file, "r")
    for line in vspace:
        line.strip().split('/n')
        if line.startswith('seed '):
            seedline = line.split()
            seed = seedline[1]
            np.random.seed(int(seed))

    # get number of files
    files = sub.check_output(
        "find %s -maxdepth 1 -mindepth 1 -type d" % folder_name, shell=True).split()
    for f in files:
        os.chdir(str(f).encode("utf-8"))
        earth = open('earth.in', "r+")

        for line in earth:
            line.strip().split('/n')

            if line.startswith('dEcc '):
                eccline = line.split()
                ecc = float(eccline[1])
                rng = 1 - ecc
                if rng < ecc:
                    EccAmp = str(np.random.uniform(
                        low=np.float(0.01), high=np.float(rng)))
                else:
                    EccAmp = str(np.random.uniform(
                        low=np.float(0.01), high=np.float(ecc)))
                texteamp = "dEccAmp      " + EccAmp + "\n"

            if line.startswith('dObliquity'):
                oblline = line.split()
                ObliqAmp = str(np.random.uniform(
                    low=np.float(5), high=np.float(oblline[1])))
                textoblamp = "dObliqAmp       " + ObliqAmp + "\n"

        earth.write(textoblamp)
        earth.write(texteamp)
        earth.close()
        os.chdir("../../")

# --------------------------------------------------------------------

def vDirSplit(srcDir, cores=1):
    # cores is 1 no need to merge directories
    if cores == 1:
        return

    if not os.path.exists(srcDir):
        print("Error")
        return

    for i in range(1, cores + 1):
        coreDir = srcDir + "_c" + str(i)
        if os.path.isdir(coreDir) == False:
            os.mkdir(coreDir)

    subDirs = os.listdir(srcDir)
    x = list(range(1, cores + 1)) * ((len(subDirs) // cores) + 1)
    x = x[0:len(subDirs)]

    for i in range(len(subDirs)):
        coreDir = srcDir + "_c" + str(x[i])
        sourceDir = os.path.join(srcDir, subDirs[i])
        destDir = os.path.join(coreDir, subDirs[i])
        shutil.move(sourceDir, destDir)

# --------------------------------------------------------------------

def moveAllFilesinDir(srcDir, dstDir):
    # Check if both the are directories
    if os.path.isdir(srcDir) and os.path.isdir(dstDir):
        # Iterate over all the files in source directory
        for filePath in glob.glob(srcDir + '/*'):
            # Move each file to destination Directory
            shutil.move(filePath, dstDir)
    else:
        print("srcDir & dstDir should be Directories")

# --------------------------------------------------------------------

def vDirMerge(srcDir, cores=1):
    # cores is 1 no need to merge directories
    if cores == 1:
        return

    for i in range(1, cores + 1):
        coreDir = srcDir + "_c" + str(i)
        moveAllFilesinDir(coreDir, srcDir)
        if len(os.listdir(coreDir)) == 0:
            os.rmdir(coreDir)

# --------------------------------------------------------------------

def run_vplanet(folder_name):
    final = '---- FINAL SYSTEM PROPERTIES ----'
    # get number of files
    files = sub.check_output("find %s -maxdepth 1 -mindepth 1 -type d" % folder_name, shell=True).split()
    for f in files:
        os.chdir(str(f).encode("utf-8"))
        if os.path.exists('tilted.log') == False:
            sub.call("vplanet vpl.in", shell=True)
        else:
            logf = open('tilted.log', 'r')
            lines = logf.readlines()
            logf.close()
            if final in lines:
                pass
            else:
                sub.call("vplanet vpl.in", shell= True)
        os.chdir("../../")

# --------------------------------------------------------------------

def multiProcess(srcDir, cores):
    print(srcDir, cores)
    # Define an output queue
    output = mp.Queue()
    # Setup a list of processes that we want to run
    processes = []
    for i  in range(1, cores+1):
        coreDir = srcDir + "_c" + str(i)
        m = mp.Process(target=run_vplanet, args=(coreDir, ))
        processes.append(m)
    # Run processes
    for p in processes:
        p.start()
    # Exit the completed processes
    for p in processes:
        p.join()

# --------------------------------------------------------------------

def main():
    project_dir = sys.argv[1]
    cores = sys.argv[2]
    if cores > mp.cpu_count():
        print("Error: the cores given are above number of actual cores")
        print("Actual amount of cores: " + str(mp.cpu_count()))

    dirList = get_VSPACE('vplanet-multiprocess/vspace_list',project_dir)

    for dirName in dirList:
        vDirSplit(dirName, cores)
        if cores > 1:
            multiProcess(dirName, cores)
        else:
            run_vplanet(dirName)
        vDirMerge(dirName, cores)

if __name__ == "__main__":
    main()
