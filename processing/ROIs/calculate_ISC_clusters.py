import glob as glob
import os
import argparse
import sys


def clusterFinder(freq, hemi, cond):
	#SurfClust -i ../fs_lowres_std-lh.gii -input alpha/ISC_lh_alpha_01.niml.dset 6 -rmm -2 -thresh_col 7 -athresh 2.32 -amm2 25
	print(f"Freq: {freq}\nHemi: {hemi}\nCond: {cond}")
	path = os.getcwd()
	
	if os.path.isdir(freq):
		os.chdir(freq)
	else:
		print(f"Directory does not exist: {freq}\nExiting")
		sys.exit(1)
	
	files = glob.glob(f"*{hemi}_*{cond}.niml.dset")
	print(files)
	
	for aFile in files:
		os.system(f"SurfClust -i {path}/../fs_lowres_std-{hemi}.gii -input {aFile} 6 -rmm -2 -thresh_col 7 -athresh 2.32 -amm2 25 -out_roidset -overwrite")
	

def main():
	parser = argparse.ArgumentParser(
		prog="calculate_ISC_clusters.py",
		description="Reads in ISC data files and makes cluster tables",
		epilog="More convenience functions by P Molfese"
	)
	
	parser.add_argument(
		'--hemi',
		help='Hemisphere: lh rh',
		nargs=1,
		required=True
	)
	parser.add_argument(
		'--freq',
		help='Frequency: alpha beta delta theta highg lowg',
		nargs=1,
		required=True
	)
	parser.add_argument(
		'--cond',
		help='Condition: pos neg',
		nargs=1,
		required=True
	)
	
	args = parser.parse_args()
	freq = args.freq[0]
	hemi = args.hemi[0]
	cond = args.cond[0]
	
	clusterFinder(freq, hemi, cond)

if __name__ == '__main__':
	main()