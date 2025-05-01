#!/usr/bin/env python3

import os
import glob as glob
import argparse

def calculateJackknifeMean(freq, hemi, subb, story=None):
	#jacknife mean correlation is the mean of all estimates
	
	allfiles = glob.glob(f"ISC*{hemi}_{freq}_{story}*.niml.dset")
	print(f"num: {len(allfiles)}")
	
	#build a 3dMean command
	baseCommand = f"3dMean -prefix meanISC_{hemi}_{freq}_{story}.niml.dset "
		
	for aStatFile in allfiles:
		baseCommand += f"{aStatFile}[{subb}] "
		
	baseCommand += "-overwrite"
	
	print(baseCommand)
	os.system(baseCommand)


def calculateJackknifeSE(freq, hemi, subb, story):
	#jacknife standard error
	
	allfiles = glob.glob(f"ISC*{hemi}_{freq}_{story}*.niml.dset")
	n = len(allfiles)
	
	#overall mean is now meanISC_{hemi}_{freq}_{story}.niml.dset
	#calculate out every single person difference from that mean
	
	for aStatFile in allfiles:
		commandString=(
			f"3dcalc -a "
			f"meanISC_{hemi}_{freq}_{story}.niml.dset "
			f"-b {aStatFile}[{subb}] "
			f"-expr '(b-a)*(b-a)' -prefix tmpSE.{aStatFile} " 
			f"-overwrite"
		)
		print(commandString)
		os.system(commandString)
		
	#now compute actual SE
	#sum deviations
	sumSquaredDeviationsCommand = f"3dMean -sum -prefix tmp.meanSE.{hemi}_{freq}_{story}.niml.dset "
		
	deviationFiles = glob.glob("tmpSE*.niml.dset")
	for aDeviation in deviationFiles:
		sumSquaredDeviationsCommand += f"{aDeviation} "
		
	print(sumSquaredDeviationsCommand)
	os.system(sumSquaredDeviationsCommand)
	
	#square the deviations
	commandSquare = f"3dcalc -a tmp.meanSE.{hemi}_{freq}_{story}.niml.dset "
	commandSquare += f"-prefix meanSE.{hemi}_{freq}_{story}.niml.dset "
	commandSquare += f"-expr 'sqrt( ({n-1}/{n})*a )' "
	commandSquare += "-overwrite"
	
	print(commandSquare)
	os.system(commandSquare)
	

def computeJackKnifeTStatistic(freq, hemi, subb, story):
	
	allfiles = glob.glob(f"ISC*{hemi}_{freq}_{story}*.niml.dset")
	n = len(allfiles)
	
	aCommand = "3dcalc "
	aCommand += f"-a meanSE.{hemi}_{freq}_{story}.niml.dset "
	aCommand += f"-b meanISC_{hemi}_{freq}_{story}.niml.dset "
	aCommand += f"-prefix meanTstat_{hemi}_{freq}_{story}.niml.dset "
	aCommand += "-expr 'b/a' "
	aCommand += '-overwrite'
	
	print(aCommand)
	os.system(aCommand)
	
	#now need to tag the dataset accordingly t-stat
	bCommand = "3drefit "
	bCommand += f"-substatpar 0 fitt {n-1} "
	bCommand += f"meanTstat_{hemi}_{freq}_{story}.niml.dset "
	
	print(bCommand)
	os.system(bCommand)
		

def main():
	parser = argparse.ArgumentParser(
		prog="9-permute_isc.py",
		description="Performs permutation of ISC values out of 3dISC",
		epilog="Special Thanks to Gang Chen for inspriation even if not used in publication"
	)

	parser.add_argument(
		'--freq',
		help='frequency',
		nargs=1,
		required=True
	)
	parser.add_argument(
		'--hemi',
		help='hemisphere',
		nargs=1,
		required=True
	)
	parser.add_argument(
		'--brikno',
		help='Sub-Brik number',
		nargs=1,
		required=True
	)
	parser.add_argument(
		'--story',
		help='Condition reflected in file name: pos neg',
		nargs=1,
		required=True
	)

	args = parser.parse_args()
	freq = args.freq[0]
	hemi = args.hemi[0]
	subb = args.brikno[0]
	story = args.story[0]
	if story is not None:
		print(f"{freq} {hemi} {subb} {story}")
	else:
		print(f"{freq} {hemi} {subb}")

	os.chdir(freq)
	
	calculateJackknifeMean(freq, hemi, subb, story)
	calculateJackknifeSE(freq, hemi, subb, story)
	computeJackKnifeTStatistic(freq, hemi, subb, story)
	
	os.system("rm tmp*")


if __name__ == '__main__':
	main()