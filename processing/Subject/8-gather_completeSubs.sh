#!/bin/bash

grpDir=/Users/molfesepj/Desktop/Ballard_MEG/Group
mkdir -p /Users/molfesepj/Desktop/Ballard_MEG/Group
dataDir=/Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/data

cd $grpDir
mkdir alpha beta delta highg lowg theta

for aS in 102 104 107 108 109 110 111 112 114 116 118 119 122 123 125 126 127 128 129 130 131 133 134 136 138 139 140 141 142 201 203 204 205 206 207 209 210 211 212 218 219 221 222 224 225 226 227 228 230
do
    cd $dataDir
    
    #rsync -avu $aS/freqStandardSurfaces/*alpha*.niml.dset $grpDir/alpha
    #rsync -avu $aS/freqStandardSurfaces/*beta*.niml.dset $grpDir/beta
    #rsync -avu $aS/freqStandardSurfaces/*delta*.niml.dset $grpDir/delta
    #rsync -avu $aS/freqStandardSurfaces/*highg*.niml.dset $grpDir/highg
    #rsync -avu $aS/freqStandardSurfaces/*lowg*.niml.dset $grpDir/lowg
    rsync -avu $aS/freqStandardSurfaces/*theta*.niml.dset $grpDir/theta
done