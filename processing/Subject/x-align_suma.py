#!/Users/molfesepj/miniconda3/envs/mne/bin/python

import mne
import numpy as np
import os
import glob
import argparse
import matplotlib.pyplot as plt
import time

def suma_align(subject):
      #hard coded until i go back and fix it
      subjects_dir='/Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/freesurfer'
      sumadir=f"{subjects_dir}/{subject}/SUMA"

      



def main():
    parser = argparse.ArgumentParser(
        prog="6-align_suma.py",
        description="Align Gifti based STCs to SUMA directory",
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

    suma_align(subj)


if __name__ == '__main__':
	main()