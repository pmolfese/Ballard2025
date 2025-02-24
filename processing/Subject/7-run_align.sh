#!/bin/bash

current=`pwd`
codeDir=/Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/code

for aS in $@
do
    echo $aS
    cd /Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/${aS}
    if [ -e freqStandardSurfaces ]; then
        echo "subject ${aS} presumably already processed"
        break
    fi
    mkdir freqStandardSurfaces
    subjDir=`pwd`
    for aFreq in alpha beta delta highg lowg theta
    do
        cd freq_${aS}_$aFreq
        for aRun in 01 02 03 04
        do
            for aHemi in lh rh
            do
                python ${codeDir}/suma_align_mne.py \
                --sub_anat ${aS}_${aRun}_${aFreq}-${aHemi}.gii \
                --sub_time ${aS}_${aRun}_${aFreq}-${aHemi}.time.gii \
                --suma_surf /Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/freesurfer/${aS}/SUMA/std.60.${aHemi}.white.gii \
                --hemi ${aHemi} \
                --output /Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/${aS}/freqStandardSurfaces

                rm /Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/${aS}/freqStandardSurfaces/center_al*.1D
                rm /Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/${aS}/freqStandardSurfaces/std.*coord.1D.dset

                mv /Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/${aS}/freqStandardSurfaces/std.60.1D \
                    /Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/${aS}/freqStandardSurfaces/std.60.${aFreq}.${aHemi}.1D

                mv /Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/${aS}/freqStandardSurfaces/std.60.niml.M2M \
                    /Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/${aS}/freqStandardSurfaces/std.60.${aFreq}.${aHemi}.niml.M2M
                
            done
        done
        cd $subjDir
        mv freq_${aS}_*/*centered.gii /Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/${aS}/freqStandardSurfaces
    done

done