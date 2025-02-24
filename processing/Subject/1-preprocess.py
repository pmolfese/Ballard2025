#!/Users/molfesepj/miniconda3/envs/mne/bin/python

import mne
import numpy as np
import os
import glob
import argparse
import time

def parseRunNum(filename):
     nameArr = filename.split("_")
     outname = nameArr[2].replace('-f.ds','')
     print(outname)
     return outname

def preprocSubj(subj):
    subject = subj
    subjects_dir="/Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/freesurfer"
    data_dir=f"/Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/{subject}"

    os.chdir(data_dir)

    #movie current files
    moviefiles = glob.glob("*movieclips*.ds")
    moviefiles.sort()
    print(moviefiles)
    #should be the same for each so going to use first

    for aMovie in moviefiles:
        raw = mne.io.read_raw_ctf(aMovie,system_clock='ignore')
        raw.load_data()

        runNo = parseRunNum(aMovie)
        print(runNo)

        print(raw)

        plot_kwargs = dict(
            subject=subject,
            subjects_dir=subjects_dir,
            surfaces="head-dense",
            dig=True,
            eeg=[],
            meg="sensors",
            show_axes=True,
            coord_frame="meg",
        )
        view_kwargs = dict(azimuth=45, elevation=90, distance=0.6, focalpoint=(0.0, 0.0, 0.0))
        kwargs = dict(eeg=False, coord_frame="meg", show_axes=True, verbose=True)

        #plot helmet
        #fig = mne.viz.plot_alignment(raw.info, meg=("helmet", "sensors", "ref"), **kwargs)
        #fig.plotter.screenshot(f"{subject}_vis_align_helmet_{runNo}.jpg")

        #alignment
        fiducials = "estimated"  # get fiducials from fsaverage
        coreg = mne.coreg.Coregistration(raw.info, subject, subjects_dir, fiducials=fiducials)
        fig = mne.viz.plot_alignment(raw.info, trans=coreg.trans, **plot_kwargs)
        fig.plotter.screenshot(f"{subject}_vis_align__{runNo}_step1.jpg")
        print(coreg.trans)

        coreg.fit_fiducials(verbose=True)
        fig = mne.viz.plot_alignment(raw.info, trans=coreg.trans, **plot_kwargs)
        fig.plotter.screenshot(f"{subject}_vis_align__{runNo}_step2.jpg")
        print(coreg.trans)

        coreg.fit_icp(n_iterations=6, nasion_weight=2.0, verbose=True)
        fig = mne.viz.plot_alignment(raw.info, trans=coreg.trans,  **plot_kwargs)
        fig.plotter.screenshot(f"{subject}_vis_align__{runNo}_step3.jpg")
        out_trans=coreg.omit_head_shape_points(distance=5.0 / 1000)  # distance is in meters
        print(out_trans)

        coreg.fit_icp(n_iterations=20, nasion_weight=10.0, verbose=True)
        fig = mne.viz.plot_alignment(raw.info, trans=coreg.trans,  **plot_kwargs)
        fig.plotter.screenshot(f"{subject}_vis_align__{runNo}_step4.jpg")

        dists = coreg.compute_dig_mri_distances() * 1e3  # in mm
        print(
            f"Distance between HSP and MRI (mean/min/max):\n{np.mean(dists):.2f} mm "
            f"/ {np.min(dists):.2f} mm / {np.max(dists):.2f} mm"
        )

        #mne.viz.set_3d_view(fig, **view_kwargs)

        dists = coreg.compute_dig_mri_distances() * 1e3  # in mm
        print(
            f"Distance between HSP and MRI (mean/min/max):\n{np.mean(dists):.2f} mm "
            f"/ {np.min(dists):.2f} mm / {np.max(dists):.2f} mm"
        )
        
        print(coreg.trans)

        #input("Press Enter to continue...")
        time.sleep(3)
        mne.write_trans(f"{data_dir}/{subject}-{runNo}_trans.fif", coreg.trans, overwrite=True)
    


def main():
    parser = argparse.ArgumentParser(
        prog="1-preprocess.py",
        description="Does alignment of MEG and Freesurfer data",
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

    preprocSubj(subj)


if __name__ == '__main__':
	main()