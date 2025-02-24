#!/bin/bash

current=`pwd`

for aS in $@
do
    cd /Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data/${aS}
    echo $aS
    for aFreq in alpha beta delta highg lowg theta
    do
        #echo $aFreq
        mkdir freq_${aS}_${aFreq}
        mv *_${aFreq}*.gii *_${aFreq}*.stc *_${aFreq}*_raw.fif freq_${aS}_${aFreq}
    done
    cd $current
done