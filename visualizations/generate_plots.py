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
	
def make_rolling_figure_2grp(mean_data, std_data, saveDir, nameFile):
	plt.figure()
	
	if not os.path.exists(saveDir):
		print(f"Directory '{saveDir}' does not exist. Creating it...")
		os.makedirs(saveDir)
	os.chdir(saveDir)
	
	
	step = 15
	
	meanMHV = mean_data["HV"] - std_data["HV"]
	meanPHV = mean_data["HV"] + std_data["HV"]
	
	meanMMDD = mean_data["MD"] - std_data["MD"]
	meanPMDD = mean_data["MD"] + std_data["MD"]
	
	plt.figure(figsize=(16, 6))
	plt.plot(mean_data.index[::step], mean_data["HV"][::step], label="HV", color="blue")
	plt.plot(mean_data.index[::step], mean_data["MD"][::step], label="MD", color="green")
	
	x = np.arange(len(mean_data)) #still silly this needs to be added
	
	plt.fill_between(x[::step], 
					 meanMHV[::step],
					 meanPHV[::step], 
					 color='green', alpha=0.2, label='HV St.Dev')
	
	plt.fill_between(x[::step], 
					 meanMMDD[::step],
					 meanPMDD[::step], 
					 color='blue', alpha=0.2, label='MDD St.Dev')
	
	plt.title('Average Time Series with Standard Deviation')
	plt.xlabel('Time')
	plt.ylabel('Source Values')
	plt.legend()
	#plt.show()
	plt.savefig(f"{nameFile}.png")

def make_average_time_plots(roi_data, saveDir):
	
	#for anROI in range(0,len(roi_data)):
	for anROI in range(0,1):
		df = roi_data[anROI]
		corr_matrix = df.corr()
		plt.figure()
		heatplot = sns.heatmap(corr_matrix, annot=False, cmap='coolwarm')
		fig = heatplot.get_figure()
		fig.savefig(f"corr_{anROI}.png")
		
		group_data = df.transpose()
		#the columns at this point say ???_??_freq
		
		group_data['subject_number'] = group_data.index.str.split('_').str[0].astype(int)
		#print(group_data)
		
		group_data['Group'] = pd.NA #probably not necessary but was getting an error in previous pandas version
		group_data['Group'] = group_data['subject_number'].apply(lambda x: 'MD' if 100 <= x < 200 else 'HV')
		
		#print(f"{group_data['subject_number']} {group_data['Group']}")
		
		groupmean = group_data.groupby('Group').mean().transpose()
		groupstd = group_data.groupby('Group').std().transpose()
		
		make_rolling_figure_2grp(groupmean, groupstd, saveDir, f"group_plot_{anROI}")
		
def make_correlation_time_plots(roi_data, outputDir):
	for anROI in range(0,1):
		df = roi_data[anROI]
		
		group_data = df.transpose()
		#the columns at this point say ???_??_freq
		
		group_data['subject_number'] = group_data.index.str.split('_').str[0].astype(int)
		#print(group_data)
		
		group_data['Group'] = pd.NA #probably not necessary but was getting an error in previous pandas version
		group_data['Group'] = group_data['subject_number'].apply(lambda x: 'MD' if 100 <= x < 200 else 'HV')
		
		#print(f"{group_data['subject_number']} {group_data['Group']}")
		
		MD_data = group_data[group_data['Group'] == 'MD']
		HV_data = group_data[group_data['Group'] == 'HV']
		
		make_rolling_figure_2grp(groupmean, groupstd, saveDir, f"group_corr_plot_{anROI}")
		
def saveROIfiles(ListofROIs, outputDir, freq, hemi):
	if not os.path.exists(outputDir):
		print(f"Directory '{outputDir}' does not exist. Creating it...")
		os.makedirs(outputDir)
	os.chdir(outputDir)
	
	ct=1
	for anROI in ListofROIs:
		anROI.to_csv(f"ROI_{freq}_{hemi}_{ct}.csv", index=False)
		ct += 1
	
	
	


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
	
	parser.add_argument(
		'--saveROI',
		help='Save ROI data to output directory',
		action='store_true'
	)
	
	parser.add_argument(
		'--outputDir',
		help='Output directory for files',
		default='tmpOut'
	)
	

	args = parser.parse_args()
	folderpath = args.roi_folder[0]
	freq = args.frequency[0]
	storyNum = args.storyNum[0]
	hemi = args.hemi[0]
	outputDir = args.outputDir
	saveROIs = args.saveROI
	
	print(folderpath)
	print(freq)
	print(storyNum)
	print(hemi)
	print(args.saveROI)
	
	cwd = os.getcwd()
	os.chdir(f"{folderpath}/{freq}")
	
	roi_data = parsedata(freq, storyNum, hemi)
	os.chdir(cwd)
	
	if saveROIs == True:
		saveROIfiles(roi_data, outputDir, freq, hemi)
	
	make_average_time_plots(roi_data, outputDir)
	
	make_correlation_time_plots(roi_data, outputDir)


if __name__ == '__main__':
	main()