#!/bin/bash

current=`pwd`

identify_brain_location() {
    echo $1
    whereami \
        -atlas MNI_Glasser_HCP_v1.0 \
        -omask $1
}

for aS in $@
do
    cd $aS
    for aFile in *.nii.gz
    do
        echo $aFile
        3drefit -space MNI -view tlrc $aFile
        identify_brain_location $aFile
    done
    cd $current
done