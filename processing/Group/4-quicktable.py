#!/usr/bin/env python3

from collections import abc
import os
import itertools as it
import argparse

def makepairs(subject_list, freq, hemi, story, tablesuffix=""):       
    #paired_140_217_rh_neg_alpha.niml.dset
    combos = it.combinations(subject_list, 2)

    if  tablesuffix == "":
        table_name = f"meg_ISC_{hemi}_{freq}_datatable_{story}.txt"
    else:
        table_name = f"meg_ISC_{hemi}_{freq}_datatable_{story}_{tablesuffix}.txt"
    
    f = open(table_name,'w')
    f.write("Subj1 Subj2 Grp InputFile \\\n")
    f.close()

    for pair in combos:
            x = pair[0]
            y = pair[1]

            if int(x) > 100 and int(x) < 200:
                cond1 = "MD"
            else:
                cond1 = "HV"

            if int(y) > 100 and int(y) < 200:
                cond2 = "MD"
            else:
                cond2 = "HV"

            if cond1 != cond2:
                cond1='HV'
                cond2='MD'
                
            if os.path.exists(f"paired_{x}_{y}_{hemi}_{story}_{freq}.niml.dset"):
                #print(f"{x} {y} {cond1}_{cond2} paired_{x}_{y}_{hemi}_{story}_{freq}.niml.dset")
                with open(table_name, "a") as text_file:
                    text_file.write(f"{x} {y} {cond1}_{cond2} paired_{x}_{y}_{hemi}_{story}_{freq}.niml.dset\n")
            else:
                if os.path.exists(f"paired_{y}_{x}_{hemi}_{story}_{freq}.niml.dset"):
                    #print(f"{y} {x} {cond1}_{cond2} paired_{x}_{y}_{hemi}_{story}_{freq}.niml.dset")
                    with open(table_name, "a") as text_file:
                        text_file.write(f"{y} {x} {cond1}_{cond2} paired_{y}_{x}_{hemi}_{story}_{freq}.niml.dset\n")
                else:
                    print(f"FILE MISSING: {x} {y}")
                    with open("MISSING_ISC_{freq}.txt", "a") as text_file:
                        text_file.write(f"FILE MISSING: {x} {y} {freq} {story} {hemi} {tablesuffix}\n")
                               
            


def main():
    parser = argparse.ArgumentParser(
        prog="4-quicktable.py",
        description="Generates 3dISC data table",
        epilog="convenience functions by P Molfese"
    )

    parser.add_argument(
        '--freq',
        help='frequency: alpha, beta, delta, theta, highg, lowg',
        nargs=1,
        required=True
    )
    parser.add_argument(
        '--story',
        help='story number: 01 02 03 04 pos neg',
        nargs=1,
        required=True
    )
    parser.add_argument(
        '--hemi',
        help='hemisphere: lh rh',
        nargs=1,
        required=True
    )
    parser.add_argument(
        '--permute',
        help='Writes tables for leave-one-out cross-validation',
        action='store_true'
    )

    a = [102, 103, 104, 108, 110, 112, 114, 116, 118, 119, 122, 123, 
        125, 126, 127, 128, 129, 131, 133, 134, 138, 139, 140, 141, 142, 
        201, 203, 204, 205, 206, 207, 210, 211, 212, 218, 219, 221, 222, 
        226, 228, 230, 216, 229, 105, 106, 120, 135, 113, 208, 213, 224]

    subjects = list(set(a)) #removes duplicates

    args = parser.parse_args()
    frequency = args.freq[0]
    os.chdir(frequency)
    print(frequency)

    if args.permute:
        leave_one_out_combinations = it.combinations(subjects, len(subjects) - 1)
        for combination in leave_one_out_combinations:
            excluded_subject = set(subjects) - set(combination)
            excluded_subject = excluded_subject.pop()
            print(f"LOOCV: {excluded_subject}")
            makepairs(combination, frequency, args.hemi[0], args.story[0], excluded_subject)
    else:
        makepairs(subjects, frequency, args.hemi[0], args.story[0])

if __name__ == '__main__':
        main()

