#!/bin/bash

module load afni

for aFreq in alpha beta delta highg lowg theta
do
	for aSub in $aFreq/???_??_${aFreq}_std-rh.time.niml.dset
	do
		echo $aSub
		#"echo ${aSub%_std-rh.time.niml.dset} RH a2009 annot"
		echo "3dROIstats -mask std.60.rh.aparc.a2009s.annot.niml.dset -quiet $aSub > roi_aparc2009/${aSub%.time.niml.dset}.txt"
		3dROIstats -mask std.60.rh.aparc.a2009s.annot.niml.dset -quiet $aSub > roi_aparc2009/${aSub%.time.niml.dset}.txt
	done
done
