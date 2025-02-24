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
     outname = nameArr[2].replace('.ds','')
     print(outname)
     return outname



def cleanSubj(subj):
    subject = subj
    subjects_dir="/Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/freesurfer"
    data_dir=f"/Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/{subject}"

    os.chdir(data_dir)

    #movie current files
    moviefiles = glob.glob("*movieclips*.ds")
    moviefiles.sort()
    print(moviefiles)
    #should be the same for each so going to use first
    #icaFile(subj, moviefiles[0])
    #for aMovie in moviefiles:
    #     icaFile(aMovie)

    # fileInput = moviefiles[0]
    for fileInput in moviefiles:
        movieNum = parseRunNum(fileInput)


        raw = mne.io.read_raw_ctf(fileInput, clean_names=True, system_clock='ignore')
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
        
        #input("Press Enter to continue...")
        #time.sleep(3)

        fig = ica.plot_components(show=False)
        fig.savefig(f"{subject}_vis_ica_components_{movieNum}.jpg")

        #can have it ask you for the components to delete!
        cdeletes = input("Enter components to delete (e.g.: 0,1): ")
        components = cdeletes.split(',')
        components2 = list(map(int, components))
        ica.exclude = components2

        print(type(components))
        components2.sort()

        reconst_raw = raw.copy()
        ica.apply(reconst_raw)
        #reconst_raw.plot(show_scrollbars=False, show=True)

        #input("Press Enter to continue...")
        time.sleep(1)

        newFname = fileInput.replace('-f.ds','_raw.fif')
        reconst_raw.save(newFname, overwrite=True)

        #read empty room and apply ICA then save
        getEmptyName = glob.glob("*EmptyRoom*.ds")
        empty_raw = mne.io.read_raw_ctf(getEmptyName[0], clean_names=True, system_clock='ignore')
        empty_raw.load_data()
        ica.apply(empty_raw)

        #save out empty 
        newEname = f"{subj}_EmptyRoom_{movieNum}_raw.fif"
        empty_raw.save(newEname, overwrite=True)

        with open(f"{subj}_ICA_removed.txt", 'a+') as f:
             f.write(f"{fileInput} {components2}\n")
    


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

    args = parser.parse_args()
    subj = args.subj[0]
    print(subj)

    cleanSubj(subj)
    #input("Press Enter to continue...")


if __name__ == '__main__':
	main()