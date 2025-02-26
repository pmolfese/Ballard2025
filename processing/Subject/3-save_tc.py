#!/Users/molfesepj/miniconda3/envs/mne/bin/python

import mne
import numpy as np
import os
import glob
import argparse
import matplotlib.pyplot as plt
from mne.preprocessing import ICA, corrmap
import time

def parseRunNum(filename):
     nameArr = filename.split("_")
     outname = nameArr[2].replace('-f','')
     print(outname)
     return outname

def savefig(subject):
    
    data_dir=f"/Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/{subject}"
    os.chdir(data_dir)

    mne.viz.set_browser_backend('matplotlib')

    moviefiles = glob.glob("*movie*_raw.fif")
    moviefiles.sort()
    print(moviefiles)

    for fileInput in moviefiles:
         movieNum = parseRunNum(fileInput)
         raw = mne.io.read_raw_fif(fileInput)
         raw.load_data()
         print(raw)
         fig = raw.plot(show_scrollbars=False, show=True, scalings=None) #scalings='auto'
         fig.savefig(f"{subject}_vis_plot_rawCLEAN_{movieNum}.png")




def main():
    parser = argparse.ArgumentParser(
        prog="3-save_tc.py",
        description="saves time course for easy viewing",
        epilog="convenience functions by P Molfese"
    )

    parser.add_argument(
        '--subj',
        help='Subject number',
        nargs=1,
        required=True
    )

    args = parser.parse_args()
    subj = args.subj[0]
    print(subj)

    savefig(subj)
    #input("Press Enter to continue...")


if __name__ == '__main__':
	main()