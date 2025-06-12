#!/bin/bash

# Function to run SurfClust for a given hemisphere, sign, folder, and frequency
make_clusters_roi() {
    hemi=$1
    sign=$2
    folder=$3
    frequency=$4
    SurfClust -i ../fsaverage_SUMA/std.141.${hemi}.white.gii \
        -input ${folder}/std.141.ISC_${hemi}_${frequency}_${sign}.niml.dset 6 \
        -thresh_col 7 \
        -rmm -2 \
        -athresh 2.02 \
        -amm2 255 \
        -out_roidset
}

# Function to run @surf_to_vol_spackle for a hemisphere, sign, folder, and frequency
surface_to_roi_volume() {
    hemi=$1
    sign=$2
    folder=$3
    frequency=$4
    @surf_to_vol_spackle \
        -spec ../suma_MNI152_2009/std.141.MNI152_2009_${hemi}.spec \
        -surfA smoothwm \
        -surfB pial \
        -surfset ${folder}/std.141.ISC_${hemi}_${frequency}_${sign}_ClstMsk_e2_a255.0.niml.dset \
        -prefix ISC_${hemi}_${frequency}_${sign}_ClstMsk_e2_a255 \
        -maskset ../suma_MNI152_2009/${hemi}.ribbon.nii.gz -datum byte
}

# Function to run whereami for a hemisphere, sign, and frequency
identify_brain_location() {
    hemi=$1
    sign=$2
    frequency=$3
    whereami \
        -atlas MNI_Glasser_HCP_v1.0 \
        -omask ISC_${hemi}_${frequency}_${sign}_ClstMsk_e2_a255.nii.gz
}

# Main pipeline execution
main() {
    folder=${1:-alpha_fsaverage}              # Default to alpha_fsaverage if not specified
    frequency=${2:-alpha}                     # Default to alpha if not specified

    # Step 1 -- make clusters ROI
    make_clusters_roi lh neg $folder $frequency
    make_clusters_roi rh neg $folder $frequency
    make_clusters_roi lh pos $folder $frequency
    make_clusters_roi rh pos $folder $frequency

    # Step 2 - surface to ROI volume (example for lh/neg)
    #3dAutomask -prefix MNI_Mask.nii MNI152_2009_SurfVol.nii

    surface_to_roi_volume lh neg $folder $frequency
    surface_to_roi_volume rh neg $folder $frequency
    surface_to_roi_volume lh pos $folder $frequency
    surface_to_roi_volume rh pos $folder $frequency

    # Step 4 - identify where in the brain (example for lh/neg)
    identify_brain_location lh neg $frequency
}

main "$@"