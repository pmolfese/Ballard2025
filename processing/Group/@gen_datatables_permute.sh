#!/bin/bash

echo "making data tables"

current=`pwd`

for aFreq in $@ #alpha beta delta highg lowg theta
do
	#swarm_3dISC_alpha_pos.txt
	#ISC_lh_alpha_neg_216.niml.dset
	#meg_ISC_lh_alpha_datatable_pos_102.txt
	#meg_run_ISC_alpha_neg_131.bash
	rm $aFreq/meg_ISC_?h_*_datatable_*_???.txt
	rm $aFreq/meg_run_ISC_*_*_???.bash
	rm $aFreq/ISC_?h_*_*_???.niml.dset
	rm $aFreq/MISSING_ISC_${aFreq}.txt
	rm $aFreq/swarm_3dISC_*.txt
done

for aFreq in $@ #alpha beta delta highg lowg theta #could also do $@ for user select
do
    for aStory in pos neg
    do
        for aHemi in lh rh
        do
            python 4-quicktable.py --freq $aFreq --story $aStory --hemi $aHemi --permute
        done
	python 3-make_ISC.py --freq $aFreq --storyNum $aStory --permute
    done
done
