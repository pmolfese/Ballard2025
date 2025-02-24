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

    #plot_bem_kwargs = dict(
    #    subject=subject,
    #    subjects_dir='/data/NIMH_Haskins/MEG/freesurfer',
    #    brain_surfaces="white",
    #    orientation="coronal",
    #    slices=[50, 100, 150, 200],
    #)

    #fig = mne.viz.plot_bem(**plot_bem_kwargs)
    #fig.savefig(f"{subject}_vis_bem.png")
    #fig = mne.viz.plot_bem(src=ss, **plot_bem_kwargs)
    #fig.savefig(f"{subject}_vis_bem.png")
    #fig = mne.viz.plot_bem(src=sv, **plot_bem_kwargs)
    #fig.savefig(f"{subject}_vis_bem-vol.png")

    #fig = mne.viz.plot_alignment(
    #    subject=subject,
    #    subjects_dir='/data/NIMH_Haskins/MEG/freesurfer',
    #    surfaces="white",
    #    coord_frame="mri",
    #    src=ss,
    #)
    #fig.plotter.screenshot(f"{subject}_vis_dipoles.jpg")

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
            src=ss,
            bem=bemsol,
            meg=True,
            eeg=False,
            mindist=5,
            n_jobs=4,
            verbose=True,
        )

        #mne.write_forward_solution(f"{subject}-fwd", fwd, overwrite=True)
        emptyRoom = mne.io.read_raw_fif(f"{subject}_EmptyRoom_{movieNum}-f_raw.fif")
        emptyRoom.load_data()
        #fig = emptyRoom.compute_psd(tmax=10).plot(
        #    average=True,
        #    spatial_colors=False,
        #    dB=False,
        #    xscale="log",
        #    picks="data",
        #    exclude="bads",
        #)
        #fig.savefig(f"{subject}_vis_emptyPSD_{movieNum}.png")

        rank_noise = mne.compute_rank(emptyRoom, tol_kind='relative', tol=1e-3)
        cov = mne.compute_raw_covariance(emptyRoom, tmin=0, tmax=None, rank=rank_noise)
        #fig = cov.plot(emptyRoom.info)
        #fig.savefig(f"{subject}_vis_emptyCOV.png")

        snr = 1
        l2 = 1.0 / snr**2 # was previously 1./9.

        inv = mne.minimum_norm.make_inverse_operator(raw.info, fwd, cov, loose=0.2)
        stc = mne.minimum_norm.apply_inverse_raw(raw, inv, lambda2=l2, method='MNE') #changed from dSPM
        stc.save(f"{subject}_{movieNum}_{freqName}", overwrite=True)

        #stc.save_as_surface(f"{subject}_{movieNum}_{freqName}", ss)

        print(f"stc_fs = mne.compute_source_morph() on {subject} {movieNum} {freqName}")

        stc_fs = mne.compute_source_morph(stc, subject_from=subject,
                                          subject_to='fsaverage',
                                          subjects_dir='/data/NIMH_Haskins/MEG/freesurfer',
                                          smooth=5,
                                          verbose="error").apply(stc)
        
        #from mne.datasets fetch_fsaverage
        #fs_dir = fetch_fsaverage(verbose=True)
        #this downloads the necessary things to subjects_dir/fsaverage
        #look at the bem folder for necessary things



        fsaverage_ss = mne.read_source_spaces(f"/data/NIMH_Haskins/MEG/freesurfer/fsaverage/bem/fsaverage-ico-5-src.fif")

        #bem_ss = f"{fs_dir}/bem/fsaverage-5120-5120-5120-bem-sol.fif"
        
        stc_fs.save_as_surface(f"{subject}_{movieNum}_{freqName}_std", fsaverage_ss)



        

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
