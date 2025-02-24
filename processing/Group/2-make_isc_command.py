import glob as glob
import os
import argparse

def makeCommand(freq, hemi, storyNum):

	#paired_{x}_{y}_lh_01_{freqency_band}
	#paired_125_227_rh_02_alpha.niml.dset

	names = glob.glob(f'paired*_{hemi}_{storyNum}_{freq}*.niml.dset')

	f = open(f'meg_ISC_{hemi}_{freq}_datatable_{storyNum}.txt','w')
	f.write(f"Subj1 Subj2 Grp InputFile \\\n")
	f.close()

	for aFile in names:
		sub1 = aFile[7:10]
		sub2 = aFile[11:14]
		#print(f"sub1: {sub1} sub2: {sub2}")

		if int(sub1) > 100 and int(sub1) < 200:
				cond1 = ('MD')
		else:
				cond1 = 'HV'
		if int(sub2) > 100 and int(sub2) < 200:
				cond2 = ('MD')
		else:
				cond2 = 'HV'
		with open (f'meg_ISC_{hemi}_{freq}_datatable_{storyNum}.txt', 'a') as text_file:
			text_file.write(f"{sub1} {sub2} {cond1}_{cond2} {aFile} \\\n")

	print(f"Wrote: meg_ISC_{hemi}_{freq}_datatable_{storyNum}.txt")


def main():
    parser = argparse.ArgumentParser(
        prog="2-make_isc_command.py",
        description="Creates your 3dISC data tables",
        epilog="convenience functions by P Molfese"
    )

    parser.add_argument(
        '--hemi',
        help='Hemisphere: lh rh',
        nargs=1,
        required=True
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
    hemi = args.hemi[0]
    story = args.storyNum[0]
    dir = args.dir[0]
    print(freq)
    print(hemi)
    print(story)

    os.chdir(dir)

    makeCommand(freq, hemi, story)


if __name__ == '__main__':
	main()
