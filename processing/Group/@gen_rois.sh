#!/bin/bash

module load afni

for aFreq in alpha beta delta highg lowg theta
do
	for aSub in $aFreq/???_??_${aFreq}_std-lh.time.niml.dset
	do
		echo "${aSub%_std-lh.time.niml.dset} LH annot"
		3dROIstats -mask std.60.lh.aparc.annot.niml.dset -quiet $aSub > roi_aparc/${aSub%.time.niml.dset}.txt
	done

	for aSub in $aFreq/???_??_${aFreq}_std-rh.time.niml.dset
	do
		echo "${aSub%_std-rh.time.niml.dset} RH annot"
		3dROIstats -mask std.60.rh.aparc.annot.niml.dset -quiet $aSub > roi_aparc/${aSub%.time.niml.dset}.txt
	done

	for aSub in $aFreq/???_??_${aFreq}_std-lh.time.niml.dset
	do
		echo "${aSub%_std-lh.time.niml.dset} LH a2009.annot"
		3dROIstats -mask std.60.lh.aparc.a2009s.annot.niml.dset -quiet $aSub > roi_aparc2009/${aSub%.time.niml.dset}.txt
	done

	for aSub in $aFreq/???_??_${aFreq}_std-rh.time.niml.dset
	do
		echo "${aSub%_std-rh.time.niml.dset} RH a2009 annot"
		#echo "3dROIstats -mask std.60.rh.aparc.a2009s.annot.niml.dset -quiet $aSub > roi_aparc2009/${aSub%.time.niml.dset}.txt"
		3dROIstats -mask std.60.rh.aparc.a2009s.annot.niml.dset -quiet $aSub > roi_aparc2009/${aSub%.time.niml.dset}.txt
	done
done
