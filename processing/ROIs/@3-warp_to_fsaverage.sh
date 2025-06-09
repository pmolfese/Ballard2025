#!/bin/bash

current=`pwd`

SUMADIR=/Users/molfesepj/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Projects/Ballard_MEG/Group_round3/fsaverage_SUMA

for aS in $@ #alpha beta delta highg lowg theta
do
	cd $aS
	
	mkdir ${current}/${aS}_fsaverage
	for aFile in *lh*.niml.dset
	do
		python ${current}/suma_align_mne.py --sub_anat ${current}/../fs_lowres_std-lh.gii --sub_time ${aFile} --suma_surf ${SUMADIR}/std.141.lh.white.gii --hemi lh --output ${current}/${aS}_fsaverage
		rm ${current}/${aS}_fsaverage/*.1D*
	done
	
	for aFile in *rh*.niml.dset
	do
		python ${current}/suma_align_mne.py --sub_anat ${current}/../fs_lowres_std-rh.gii --sub_time ${aFile} --suma_surf ${SUMADIR}/std.141.rh.white.gii --hemi rh --output ${current}/${aS}_fsaverage
		rm ${current}/${aS}_fsaverage/*.1D*
	done
	
	cd $current
done

#python suma_align_mne.py --sub_anat ../fs_lowres_std-lh.gii --sub_time alpha/ISC_lh_alpha_neg.niml.dset --suma_surf ../fsaverage_SUMA/lh.white.gii --hemi lh --output test

