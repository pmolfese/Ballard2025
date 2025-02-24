#!/data/molfesepj/conda/envs/mne/bin/python

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

def filtsubj(subject):
    data_dir=f"/data/NIMH_Haskins/MEG/data/{subject}"
    os.chdir(data_dir)
    moviefiles = glob.glob("*movie*_raw.fif")
    moviefiles.sort()
    print(moviefiles)

    for fileInput in moviefiles:
        movieNum = parseRunNum(fileInput)
        raw = mne.io.read_raw_fif(fileInput)
        raw.load_data()
        print(raw)

        delta = raw.pick(picks='meg').copy().filter(l_freq=0.5, h_freq=4, n_jobs=4)
        theta = raw.pick(picks='meg').copy().filter(l_freq=4, h_freq=8, n_jobs=4)
        alpha = raw.pick(picks='meg').copy().filter(l_freq=8, h_freq=12, n_jobs=4)
        beta = raw.pick(picks='meg').copy().filter(l_freq=12, h_freq=25, n_jobs=4)
        lowg = raw.pick(picks='meg').copy().filter(l_freq=25, h_freq=55, n_jobs=4)
        highg = raw.pick(picks='meg').copy().filter(l_freq=65, h_freq=90, n_jobs=4)

        print("Applying Hilbert...")
        delta.apply_hilbert(envelope=True)
        theta.apply_hilbert(envelope=True)
        alpha.apply_hilbert(envelope=True)
        beta.apply_hilbert(envelope=True)
        lowg.apply_hilbert(envelope=True)
        highg.apply_hilbert(envelope=True)

        delta_rs = delta.copy().filter(l_freq=0.3, h_freq=None).resample(sfreq=10)
        theta_rs = theta.copy().filter(l_freq=0.3, h_freq=None).resample(sfreq=10)
        alpha_rs = alpha.copy().filter(l_freq=0.3, h_freq=None).resample(sfreq=10)
        beta_rs = beta.copy().filter(l_freq=0.3, h_freq=None).resample(sfreq=10)
        lowg_rs = lowg.copy().filter(l_freq=0.3, h_freq=None).resample(sfreq=10)
        highg_rs = highg.copy().filter(l_freq=0.3, h_freq=None).resample(sfreq=10)

        delta_rs.save(f"{subject}_{movieNum}_delta_raw.fif", overwrite=True)
        theta_rs.save(f"{subject}_{movieNum}_theta_raw.fif", overwrite=True)
        alpha_rs.save(f"{subject}_{movieNum}_alpha_raw.fif", overwrite=True)
        beta_rs.save(f"{subject}_{movieNum}_beta_raw.fif", overwrite=True)
        lowg_rs.save(f"{subject}_{movieNum}_lowg_raw.fif", overwrite=True)
        highg_rs.save(f"{subject}_{movieNum}_highg_raw.fif", overwrite=True)

def main():
    parser = argparse.ArgumentParser(
        prog="3-freq-fit.py",
        description="source analysis by frequeny band",
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

    filtsubj(subj)


if __name__ == '__main__':
	main()
