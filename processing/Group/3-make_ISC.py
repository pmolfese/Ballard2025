
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

def makeCommand(freq, story):
    for aHemi in ["lh", "rh"]:
        f = open(f'meg_run_ISC_{freq}_{story}.bash','a')
        f.write(f"3dISC -prefix ISC_{aHemi}_{freq}_{story}.niml.dset -jobs 12 \\\n")
        f.write(f"-model '0+Grp+(1|Subj1)+(1|Subj2)' \\\n")
        f.write(f"-gltCode Grp_HV '1 0 0' \\\n")
        f.write(f"-gltCode Grp_HVMD '0 1 0' \\\n")
        f.write(f"-gltCode Grp_MD '0 0 1' \\\n")
        f.write(f"-gltCode Grp_HV-MD '1 0 -1' \\\n")
        f.write(f"-gltCode Grp_HV-Mix '1 -1 0' \\\n")
        f.write(f"-gltCode Grp_Mix-MD '0 1 -1' \\\n")
        f.write(f"-dataTable @meg_ISC_{aHemi}_{freq}_datatable_{story}.txt\n")
        f.write("\n\n")
        f.close()
        print(f"Wrote: meg_run_ISC_{freq}_{story}.bash")
      

def main():
    parser = argparse.ArgumentParser(
        prog="3-make_ISC.py",
        description="Creates your 3dISC command & runs",
        epilog="convenience functions by P Molfese"
    )

    parser.add_argument(
        '--storyNum',
        help='Story number: 01 02 03 04',
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
        '--dir',
        help='Directory to change into',
        nargs=1,
        required=True
    )



    args = parser.parse_args()
    freq = args.freq[0]
    story = args.storyNum[0]
    dir = args.dir[0]
    print(freq)
    print(story)

    os.chdir(dir)

    makeCommand(freq, story)


if __name__ == '__main__':
	main()