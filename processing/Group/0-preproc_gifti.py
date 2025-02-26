#!/usr/bin/env python 

import glob
import os
import argparse

def createScriptFile(freq):
    f = open(f'0-positive_{freq}.bash','w')
    f.write(f"#!/bin/bash \n")
    
    f.write(f"\n")
    f.write(f"module load afni\n") #specific to slurm
    
    f.write(f"\n")
    
    f.write(f"for aS in $@\n") #for loop for arguments
    f.write(f"do\n")
    
    #absolute value and make values large enough that AFNI doesn't worry
    f.write("\t3dcalc -a $aS -expr 'abs(a)*100000000000' -prefix tmp1.${aS%.gii}.niml.dset \n")
    #count outliers
    f.write("\t3dToutcount -automask -fraction -polort 4 -legendre tmp1.${aS%.gii}.niml.dset > tmp2.outcount.${aS%.gii}.1D\n")
    #if more than 15% of vertices outliers, zero
    f.write("\t1deval -a tmp2.outcount.${aS%.gii}.1D -expr '1-step(a-0.15)' > tmp3.out.cen.${aS%.gii}.1D\n")
    #apply that True/False logic to dataset
    f.write("\t3dcalc -a tmp1.${aS%.gii}.niml.dset -b tmp3.out.cen.${aS%.gii}.1D -expr 'a*b' -prefix ${aS%.gii}.niml.dset\n")
    #count the number of outliers
    f.write("\tval=`3dTstat -prefix stdout: -zcount tmp3.out.cen.${aS%.gii}.1D\'`\n")
    #print that outlier count into a handy file for later reference
    f.write("\techo \"${aS%.time.gii} $val\" >> outlier_count.1D\n")
    #remove temporary files
    f.write("\trm tmp*${aS%.gii}*\n")
    #close out for loop
    f.write(f"done\n")
    
    

def prepareFiles(freq):
    os.chdir(freq)
    os.system(f"cp ../0-positive_{freq}.bash .") #messy but quick

    files = glob.glob(f"*.gii")

    if os.path.exists(f"outlier_count.1D"):
        os.remove(f"outlier_count.1D")

    if os.path.exists(f"swarm_step1_{freq}.txt"):
        os.remove(f"swarm_step1_{freq}.txt")

    f = open(f'swarm_step1_{freq}.txt','w')

    for aFile in files:
    	f.write(f"bash 0-positive.bash {aFile}\n")

    f.close()

    os.system(f"swarm -f swarm_step1_{freq}.txt -t 2 -g 12 --logdir ../logs --job-name step1_{freq} -b 20 --time 00:07:00 --module afni --partition=quick,norm")

def main():
    parser = argparse.ArgumentParser(
        prog="0-preproc_gifti.py",
        description="Basic prep for GIFTI surface functional data",
        epilog="P Molfese for Ballard et al. 2025"
    )

    parser.add_argument(
        '--freq',
        help='frequency: alpha, beta, delta, highg, lowg, theta',
        nargs=1,
        required=True
    )

    args = parser.parse_args()
    freq = args.freq[0]

    print(freq)

    createScriptFile(freq)
    prepareFiles(freq)


if __name__ == '__main__':
	main()
