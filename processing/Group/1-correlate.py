import itertools as it
import argparse
import os


def makepairs(subject_list, frequency_band):

	combos = it.combinations(subject_list, 2)

	os.system(f"rm swarm_correlate_{frequency_band}.txt")

	for pair in combos:
		x = pair[0]
		y = pair[1]
		print(f"3dTcorrelate -zcensor -polort -1 -prefix paired_{x}_{y}_lh_{frequency_band} {x}_01_{frequency_band}_std-lh.time.niml.dset {y}_01_{frequency_band}_std-lh.time.niml.dset")
		with open(f"swarm_correlate_{frequency_band}.txt", "a") as text_file:
			text_file.write(f"3dTcorrelate -zcensor -polort -1 -prefix paired_{x}_{y}_lh_01_{frequency_band} {x}_01_{frequency_band}_std-lh.time.niml.dset {y}_01_{frequency_band}_std-lh.time.niml.dset\n")
			text_file.write(f"3dTcorrelate -zcensor -polort -1 -prefix paired_{x}_{y}_rh_01_{frequency_band} {x}_01_{frequency_band}_std-rh.time.niml.dset {y}_01_{frequency_band}_std-rh.time.niml.dset\n")
			text_file.write(f"3dTcorrelate -zcensor -polort -1 -prefix paired_{x}_{y}_lh_02_{frequency_band} {x}_02_{frequency_band}_std-lh.time.niml.dset {y}_02_{frequency_band}_std-lh.time.niml.dset\n")
			text_file.write(f"3dTcorrelate -zcensor -polort -1 -prefix paired_{x}_{y}_rh_02_{frequency_band} {x}_02_{frequency_band}_std-rh.time.niml.dset {y}_02_{frequency_band}_std-rh.time.niml.dset\n")
			text_file.write(f"3dTcorrelate -zcensor -polort -1 -prefix paired_{x}_{y}_lh_03_{frequency_band} {x}_03_{frequency_band}_std-lh.time.niml.dset {y}_03_{frequency_band}_std-lh.time.niml.dset\n")
			text_file.write(f"3dTcorrelate -zcensor -polort -1 -prefix paired_{x}_{y}_rh_03_{frequency_band} {x}_03_{frequency_band}_std-rh.time.niml.dset {y}_03_{frequency_band}_std-rh.time.niml.dset\n")
			text_file.write(f"3dTcorrelate -zcensor -polort -1 -prefix paired_{x}_{y}_lh_04_{frequency_band} {x}_04_{frequency_band}_std-lh.time.niml.dset {y}_04_{frequency_band}_std-lh.time.niml.dset\n")
			text_file.write(f"3dTcorrelate -zcensor -polort -1 -prefix paired_{x}_{y}_rh_04_{frequency_band} {x}_04_{frequency_band}_std-rh.time.niml.dset {y}_04_{frequency_band}_std-rh.time.niml.dset\n")


def make_swarm(freq):
    os.system(f"swarm -f swarm_correlate_{freq}.txt -t 2 -g 12 --logdir ../logs --job-name {freq}-proc -b 45 --time 00:05:00 --module afni --partition=quick,norm")

def main():
    parser = argparse.ArgumentParser(
        prog="1-preprocess.py",
        description="Does some alignment stuff",
        epilog="convenience functions by P Molfese"
    )

    parser.add_argument(
        '--freq',
        help='frequency: alpha, beta, delta, theta, highg, lowg',
        nargs=1,
        required=True
    )

    a = [102, 103, 104, 108, 110, 111, 112, 114, 116, 118, 119, 122, 123, 
	    125, 126, 127, 128, 129, 130, 131, 133, 134, 138, 139, 140, 141, 142, 
    	201, 203, 204, 205, 206, 207, 209, 210, 211, 212, 218, 219, 221, 222, 
    	225, 226, 228, 230, 216, 229, 105, 106, 120, 135]

    all_subs = list(set(a))


#    all_subs = [102, 104, 108, 110, 111, 112, 114, 116, 118, 119, 122, 123, 
#                         125, 126, 127, 128, 129, 130, 131, 133, 134, 138, 139, 140, 141, 142, 
#                         201, 203, 204, 205, 206, 207, 209, 210, 211, 212, 218, 219, 221, 222, 224, 
#                         225, 226, 228, 230, 103, 120, 135, 216, 229]

    args = parser.parse_args()
    frequency = args.freq[0]
    #dirToRun = args.dir[0]
    os.chdir(frequency)
    print(frequency)

    makepairs(all_subs, frequency)

    make_swarm(frequency)


if __name__ == '__main__':
	main()
