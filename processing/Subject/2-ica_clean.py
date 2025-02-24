#!/Users/molfesepj/miniconda3/envs/mne/bin/python

import mne
import numpy as np
import os
import glob
import argparse
import matplotlib.pyplot as plt
from mne.preprocessing import ICA, corrmap

def cleanSubj(subj, emptyRoom):
    subject = subj
    subjects_dir="/Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/freesurfer"
    data_dir=f"/Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/{subject}"

    os.chdir(data_dir)

    #movie current files
    moviefiles = glob.glob("*.ds")
    print(moviefiles)
    #should be the same for each so going to use first
    #icaFile(subj, moviefiles[0])
    #for aMovie in moviefiles:
    #     icaFile(aMovie)

    fileInput = moviefiles[0]


    raw = mne.io.read_raw_ctf(fileInput)
    raw.load_data()

    print(raw)
    #start ICA cleaning
    filt_raw = raw.copy().filter(l_freq=1.0, h_freq=None)
    ica = ICA(n_components=15, max_iter="auto", random_state=97)
    ica.fit(filt_raw)
    print(ica)

    explained_var_ratio = ica.get_explained_variance_ratio(filt_raw)
    for channel_type, ratio in explained_var_ratio.items():
        print(
            f"Fraction of {channel_type} variance explained by all components: " f"{ratio}"
        )
    
    raw.load_data()
    fig = ica.plot_sources(raw, show_scrollbars=False, show=True)
    
    input("Press Enter to continue...")

    fig = ica.plot_components(show=False)
    fig.savefig(f"{subject}_ica_components.jpg")

    #can have it ask you for the components to delete!
    cdeletes = input("Enter components to delete (e.g.: 0,1): ")
    components = cdeletes.split(',')
    components2 = list(map(int, components))
    print(f"Now removing components: {components2}")
    ica.exclude = components2

    reconst_raw = raw.copy()
    ica.apply(reconst_raw)
    reconst_raw.plot(show_scrollbars=False, show=True)

    input("Press Enter to continue...")

    newFname = fileInput.replace('-f.ds','raw.fif')
    reconst_raw.save(newFname)
    
    


def main():
    parser = argparse.ArgumentParser(
        prog="2-ica_clean.py",
        description="cleans task and empty room data with ICA",
        epilog="convenience functions by P Molfese"
    )

    parser.add_argument(
        '--subj',
        help='Subject number',
        nargs=1,
        required=True
    )

    parser.add_argument(
        '--empty',
        help='Empty Room Recording',
        nargs=1,
        required=True
    )

    args = parser.parse_args()
    subj = args.subj[0]
    emptyRoom = args.empty[0]
    print(subj)

    cleanSubj(subj, emptyRoom)


if __name__ == '__main__':
	main()