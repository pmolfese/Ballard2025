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
     outname = nameArr[1]
     return outname

def parseRunFreq(filename):
     nameArr = filename.split("_")
     outname = nameArr[2]
     return outname

def sourcesubj(subject):
    data_dir=f"/data/NIMH_Haskins/MEG/data/{subject}"
    os.chdir(data_dir)

    ss = mne.read_source_spaces(f"{subject}-src.fif")
    sv = mne.read_source_spaces(f"{subject}-vol-src.fif")
    bem = mne.read_bem_surfaces(f"{subject}-bem.fif")
    bemsol = mne.read_bem_solution(f"{subject}-bem-sol.fif")

    moviefiles = glob.glob('*alpha_raw.fif') + glob.glob('*beta_raw.fif') + glob.glob('*delta_raw.fif') + glob.glob('*highg_raw.fif') + glob.glob('*lowg_raw.fif') + glob.glob('*theta_raw.fif')
    moviefiles.sort()
    print(moviefiles)

    for fileInput in moviefiles:
        movieNum = parseRunNum(fileInput)
        print(movieNum)
        freqName = parseRunFreq(fileInput)
        print(freqName)
        raw = mne.io.read_raw_fif(fileInput)
        raw.load_data()
        print(raw)

        
        fwd = mne.make_forward_solution(
            raw.info,
            trans=f"{subject}-{movieNum}_trans.fif",
            src=sv,
            bem=bemsol,
            meg=True,
            eeg=False,
            mindist=0,
            n_jobs=4,
            verbose=True,
        )

        #mne.write_forward_solution(f"{subject}-fwd", fwd, overwrite=True)
        emptyRoom = mne.io.read_raw_fif(f"{subject}_EmptyRoom_{movieNum}-f_raw.fif")
        emptyRoom.load_data()

        rank_noise = mne.compute_rank(emptyRoom, tol_kind='relative', tol=1e-3)
        cov = mne.compute_raw_covariance(emptyRoom, tmin=0, tmax=None, rank=rank_noise)
        inv = mne.minimum_norm.make_inverse_operator(raw.info, fwd, cov, loose="auto")
        stc = mne.minimum_norm.apply_inverse_raw(raw, inv, lambda2=1. / 9., method='dSPM')
        print(f"Saving: {subject}_{movieNum}_{freqName}_vol")
        stc.save(f"{subject}_{movieNum}_{freqName}_vol", overwrite=True)
        stc.save_as_volume(f"{subject}_{movieNum}_{freqName}_vol", src=inv["src"], overwrite=True)
        #stc.save_as_surface(f"{subject}_{movieNum}_{freqName}", ss)


        stc_fs = mne.compute_source_morph(inv["src"], subject_from=subject,
                                           subject_to='fsaverage',
                                           subjects_dir='/data/NIMH_Haskins/MEG/freesurfer',
                                           niter_affine=[10, 10, 5],
                                           niter_sdr=[5, 5, 3],
                                           verbose="error")
                                           
        #stc_fsaverage = stc_fs.apply(stc)
        #stc_fsaverage.save(f"{subject}_{movieNum}_{freqName}_vol_std", overwrite=True)
        #stc_fsaverage.save_as_volume(f"{subject}_{movieNum}_{freqName}_vol_std", src=sv, overwrite=True)
         

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

    sourcesubj(subj)


if __name__ == '__main__':
	main()
