
import glob as glob
import os
import argparse

#3dISC -prefix ISC_lh_story01_beta.niml.dset -jobs 12 \
#-model '0+Grp+(1|Subj1)+(1|Subj2)' \
#-gltCode Grp_Control '1 0 0' \
#-gltCode Grp_ControlExp '0 1 0' \
#-gltCode Grp_Exp '0 0 1' \
#-gltCode Grp_Control-Exp '1 0 -1' \
#-gltCode Grp_Control-CE '1 -1 0' \
#-gltCode Grp_CE-Exp '0 1 -1' \
#-dataTable @meg_ISC_LH_beta_datatable.txt

#meg_ISC_{hemi}_{freq}_datatable_{storyNum}.txt



def makeCommand(freq, story, suffix=None):
    for aHemi in ["lh", "rh"]:
        if suffix is not None:
            isc_filename = f'meg_run_ISC_{freq}_{story}_{suffix}.bash'
        else:
            isc_filename = f'meg_run_ISC_{freq}_{story}.bash'
        
        f = open(isc_filename,'a')
        f.write(f"export TMPDIR=/lscratch/$SLURM_JOB_ID \n")
        f.write("\n")
        f.write("module load afni \n")
        f.write("module load R \n")
        f.write("\n")
        if suffix is not None:
            f.write(f"3dISC -prefix ISC_{aHemi}_{freq}_{story}_{suffix}.niml.dset -jobs 12 \\\n")
        else:
            f.write(f"3dISC -prefix ISC_{aHemi}_{freq}_{story}.niml.dset -jobs 12 \\\n")
        f.write(f"-model '0+Grp+(1|Subj1)+(1|Subj2)' \\\n")
        f.write(f"-gltCode Grp_HV '1 0 0' \\\n")
        f.write(f"-gltCode Grp_HVMD '0 1 0' \\\n")
        f.write(f"-gltCode Grp_MD '0 0 1' \\\n")
        f.write(f"-gltCode Grp_HV-MD '1 0 -1' \\\n")
        f.write(f"-gltCode Grp_HV-Mix '1 -1 0' \\\n")
        f.write(f"-gltCode Grp_Mix-MD '0 1 -1' \\\n")
        if suffix is not None:
            f.write(f"-dataTable @meg_ISC_{aHemi}_{freq}_datatable_{story}_{suffix}.txt\n")
        else:
            f.write(f"-dataTable @meg_ISC_{aHemi}_{freq}_datatable_{story}.txt\n")
        f.write("\n\n")
        f.close()
        print(f"Wrote: {isc_filename}")

      

def findDataTables(story, freq):
    #meg_ISC_rh_alpha_datatable_pos_139.txt
    dts = glob.glob(f'meg_ISC_lh_{freq}_datatable_{story}_*') #just get the left, generalize
    suffixes = [file.split('_')[-1].replace('.txt','') for file in dts]
    print(suffixes)
        
    for aFile in suffixes:
        makeCommand(freq, story, suffix=aFile)
        with open(f"swarm_3dISC_{freq}_{story}.txt", "a") as text_file:
            isc_filename = f'meg_run_ISC_{freq}_{story}_{aFile}.bash'
            text_file.write(f"bash {isc_filename}\n")

    print(f"swarm -f swarm_3dISC_{freq}_{story}.txt -t 12 -g 16 --logdir ../logs --job-name isc_{freq}_{story} -b 2 --time 00:20:00 --module afni,R --partition=quick,norm")
    os.system(f"swarm -f swarm_3dISC_{freq}_{story}.txt -t 12 -g 16 --logdir ../logs --job-name isc_{freq}_{story} -b 2 --time 00:20:00 --module afni,R --partition=quick,norm")
        

def main():
    parser = argparse.ArgumentParser(
        prog="3-make_ISC.py",
        description="Creates your 3dISC command & runs",
        epilog="convenience functions by P Molfese"
    )
    parser.add_argument(
        '--storyNum',
        help='Story number: 01 02 03 04 pos neg',
        nargs=1,
        required=True
    )
    parser.add_argument(
        '--freq',
        help='Frequency to use: alpha, beta, theta, delta, highg, lowg',
        nargs=1,
        required=True
    )
    parser.add_argument(
        '--permute',
        help='looks for datatables that exist and writes a 3dISC for each',
        action='store_true'
    )



    args = parser.parse_args()
    freq = args.freq[0]
    story = args.storyNum[0]
    dir = freq
    print(freq)
    print(story)

    os.chdir(dir)

    if args.permute:
        print("Looking for DataTables to permute on")
        findDataTables(story, freq)
    else:
        makeCommand(freq, story)


if __name__ == '__main__':
	main()