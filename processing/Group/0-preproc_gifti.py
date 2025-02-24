#!/usr/bin/env python 

import glob
import os
import argparse

def prepareFiles(freq):
    os.chdir(freq)
    os.system(f"cp ../0-positive.bash .") #messy but quick

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

    prepareFiles(freq)


if __name__ == '__main__':
	main()
