import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import glob
import argparse

def getShapeFile(aFile):
	tmp = pd.read_csv(aFile, sep='\t', header=None)
	tmp = tmp.drop(tmp.columns[0], axis=1)
	print(f"Number ROIs: {tmp.shape[1]}")
	return tmp.shape[1]
	
def readROIFiles(filesArr, ROInumber):
	my_col = pd.DataFrame()
	for aFile in filesArr:
		df = pd.read_csv(aFile, sep='\t', header=None)
		df = df.drop(df.columns[0], axis=1) #drops empty first col
		
		#get selected col (0-based index)
		col_selected = df[df.columns[ROInumber]]
		my_col = pd.concat([my_col, col_selected], ignore_index=True, axis=1)
	
	renamedList = [x.replace('.txt','') for x in filesArr]
	renamedList = [x.replace('_std','') for x in renamedList]
	renamedList = [x.replace('_std','') for x in renamedList]
	renamedList = [x.replace(f"-lh",'') for x in renamedList]
	renamedList = [x.replace(f"-rh",'') for x in renamedList]
	my_col.columns = renamedList
	#print(renamedList)
	
	return my_col


def parsedata(freq, storyNum, hemi):
	all_files = glob.glob(f"*_{storyNum}_{freq}_std-{hemi}.txt")
	all_files.sort()
	
	numROIs = getShapeFile(all_files[0])
	
	rois = []
	for anROInumber in range(0,numROIs):
		datamatrix = readROIFiles(all_files, anROInumber)
		rois.append(datamatrix)
		print(f"Read ROI: {anROInumber}")
	
	return rois

def make_average_time_plots(roi_data):
	
	#for anROI in range(0,len(roi_data)):
	for anROI in range(0,1):
		df = roi_data[anROI]
		
		print(df)
		print(type(df))
		print(df.shape)
		corr_matrix = df.corr()
		#print(corr_matrix)
		#print(corr_matrix.shape)
		plt.figure()
		heatplot = sns.heatmap(corr_matrix, annot=False, cmap='coolwarm')
		fig = heatplot.get_figure()
		fig.savefig(f"corr_{anROI}.png")
		
		
		
		
		


def main():
	parser = argparse.ArgumentParser(
		prog="generate_plots.py",
		description="Create plots for source activation and correlation by region",
		epilog="convenience functions by P Molfese"
	)

	parser.add_argument(
		'--roi_folder',
		help='Path to folder containing ROIs',
		nargs=1,
		required=True
	)
	
	parser.add_argument(
		'--frequency',
		help='Frequency subfolder within ROI folder: alpha, beta, delta, highg, lowg, theta',
		nargs=1,
		required=True
	)
	
	parser.add_argument(
		'--storyNum',
		help='Story Number: 00-04',
		nargs=1,
		required=True
	)
	
	parser.add_argument(
		'--hemi',
		help='Hemisphere: lh, rh',
		nargs=1,
		required=True
	)
	

	args = parser.parse_args()
	folderpath = args.roi_folder[0]
	freq = args.frequency[0]
	storyNum = args.storyNum[0]
	hemi = args.hemi[0]
	
	print(folderpath)
	print(freq)
	print(storyNum)
	print(hemi)
	
	cwd = os.getcwd()
	os.chdir(f"{folderpath}/{freq}")
	
	roi_data = parsedata(freq, storyNum, hemi)
	os.chdir(cwd)
	make_average_time_plots(roi_data)
	#make_correlation_time_plots(roi_data)


if __name__ == '__main__':
	main()