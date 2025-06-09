#!/bin/bash

#hemi $1

export LIBGL_ALWAYS_SOFTWARE=YES

DriveSuma -com viewer_cont -key "F3"
DriveSuma -com viewer_cont -key "F4"
DriveSuma -com viewer_cont -key "F5"
DriveSuma -com viewer_cont -key "F6"

for aFreq in alpha beta delta highg lowg theta
do
    for aStory in pos neg
    do
        DriveSuma -com viewer_cont -key "ctrl+alt+left"
        echo "DriveSuma -com surf_cont -load_dset ${aFreq}/ISC_${1}_${aFreq}_${aStory}.niml.dset"
        DriveSuma -com surf_cont -load_dset ${aFreq}/ISC_${1}_${aFreq}_${aStory}.niml.dset
        sleep 1
        DriveSuma -com surf_cont -I_sb 6
        DriveSuma -com surf_cont -T_sb 7
        sleep 2
        DriveSuma -com surf_cont -T_val 0.025p
        sleep 2
        DriveSuma -com viewer_cont -key r
        sleep 1
        DriveSuma -com recorder_cont -save_as result_${aFreq}_${aStory}_${1}_left.jpg
        sleep 1
        DriveSuma -com viewer_cont -key "ctrl+alt+right"
        DriveSuma -com viewer_cont -key r
        sleep 1
        DriveSuma -com recorder_cont -save_as result_${aFreq}_${aStory}_${1}_right.jpg
        sleep 1
        
    done
done
