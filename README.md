# Ballard2025
Code for processing MEG data in Ballard et al. 2025 (currently in prep)

Group

	0-preproc_gifti.py: preprocesses GIFTI surfaces
	- creates processing bash script
	- censors out time points with more than 15% of outliers
	- Keeps track of number censored volumes
	
	1-correlate.py: does pairwise correlations across all subjects
	- takes a list of "good" subjects
	- does pairwise matching
	- generates a swarm file to run AFNI's 3dTcorrelate on each pair
	- executes the swarm file on the cluster
	
	2-make_isc_command.py: creates a DataTable for use with 3dISC
	- looks at all data files in the source directory
	- figures out if the mix is same group (MD-MD; HV-HV) or mixed (HV-MD)
	- writes a 3dISC data table file
	- this script was replaced with 4-quicktable.py
	
	3-make_ISC.py: Creates 3dISC command
	- Takes list of story number, frequency and makes required file
	
Misc

	suma_align_mne.py: aligns decimated surface with high-res corresponding one
	- used in earlier pipelines, not necessary if warping to fsaverage in MNE
	- helpful if you want to transform freesurfer aparc files to decimated surfaces

Subject

	0-setup_sources.py: wrapper script to create source models
	- Assumes you've already run Freesurfer on anatomical MRIs
	- Has options for EEG or MEG conductivity
	- Can turn on/off watershed, BEM, source space
	- default is to run everything for MEG
	- also generates useful QC images via Freeview
	
	1-preprocess.py: 