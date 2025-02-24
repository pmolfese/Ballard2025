#!/Users/molfesepj/miniconda3/envs/mne/bin/python

import mne
import numpy as np
import os
import glob
import subprocess
import argparse

###
#python suma_align_mne.py \
#--sub_lh demo/102_01_alpha-lh.gii \
#--sub_rh demo/102_01_alpha-rh.gii \
#--sub_time_lh demo/102_01_alpha-lh.time.gii \
#--sub_time_rh demo/102_01_alpha-rh.time.gii \
#--sumadir demo/102/SUMA
####

def getSurfMetrics(aSurface):
    #step 1 & 3 - gets called on both initial surface and standard surface
    check = subprocess.call(["SurfaceMetrics","-i",aSurface,"-coords"])
    newname=f"{aSurface}.coord.1D.dset"
    newname=os.path.basename(newname)

    #Step 2
    #get center coordinates
    #centerX=`3dBrickStat -mean myhead-lh.gii.coord.1D.dset[1]`
    centerX = subprocess.run(["3dBrickStat","-mean",f"{newname}[1]"], capture_output=True, text=True).stdout.strip()
    #centerY=`3dBrickStat -mean myhead-lh.gii.coord.1D.dset[2]`
    centerY = subprocess.run(["3dBrickStat","-mean",f"{newname}[2]"], capture_output=True, text=True).stdout.strip()
    #centerZ=`3dBrickStat -mean myhead-lh.gii.coord.1D.dset[3]`
    centerZ = subprocess.run(["3dBrickStat","-mean",f"{newname}[3]"], capture_output=True, text=True).stdout.strip()

    #print(f"X: {centerX} Y:{centerY} Z:{centerZ}")

    return [centerX, centerY, centerZ]


def calculateListDiff(surfA, surfB):
    #Step 4
    centerDiff=[]
    for mydx in range(0,3):
        centerDiff.append(round((float(surfB[mydx]) - float(surfA[mydx])),6))
    #print(centerDiff)
    return centerDiff

def makeTransformCenter(centerArr, hemi):
     #step 4
     f = open(f"center_al_transform_{hemi}.1D", 'w')
     f.write(f"1 0 0 {centerArr[0]}")
     f.write('\n')
     f.write(f"0 1 0 {centerArr[1]}")
     f.write('\n')
     f.write(f"0 0 1 {centerArr[2]}")
     f.write('\n')
     f.close()

def createSurfAndAlign(anatS, timeS, sumaS, hemi):
    #Step 5 & 6
    print("Creating Surface with Transform")
    centeredTransform = f"center_al_transform_{hemi}.1D"
    print(centeredTransform)
    outputAnatS = anatS.replace('.gii',"-centered.gii")
    print(outputAnatS)
    subprocess.call(["ConvertSurface", "-xmat_1D", f"{centeredTransform}", "-i", f"{anatS}", "-o", f"{outputAnatS}"])
    #print("Running SurfToSurf")
    subprocess.call(["SurfToSurf", "-i_gii", f"{sumaS}", "-i_gii", f"{outputAnatS}", "-dset", f"{timeS}", "-prefix", "std.60."])

def suma_align(anatS, timeS, sumaS, hemi):
    #get center of input anatomical surface
    anatCenter = getSurfMetrics(anatS)
    sumaCenter = getSurfMetrics(sumaS)
    print(f"MNE Center: x={anatCenter[0]} y={anatCenter[1]} z={anatCenter[2]}")
    print(f"SUMA Center: x={sumaCenter[0]} y={sumaCenter[1]} z={sumaCenter[2]}")
    centerShift = calculateListDiff(anatCenter, sumaCenter)
    print(f"Center Differences: {centerShift}")
    makeTransformCenter(centerShift, hemi)
    createSurfAndAlign(anatS, timeS, sumaS, hemi)
     

def main():
    parser = argparse.ArgumentParser(
        prog="suma_align_mne.py",
        description="Align Gifti based STCs to SUMA directory",
        epilog="Convenience functions by P Molfese"
    )
    parser.add_argument(
        '--sub_anat',
        help='Decimated Anatomical Surface',
        nargs=1,
        required=True
    )
    parser.add_argument(
        '--sub_time',
        help='Surface Timeseries',
        nargs=1,
        required=True
    )
    parser.add_argument(
        '--suma_surf',
        help='SUMA Directory Surface to Align',
        nargs=1,
        required=True
    )
    parser.add_argument(
        '--hemi',
        help='Hemisphere (lh/rh) to label files correctly',
        nargs=1,
        required=True
    )
    parser.add_argument(
        '--output',
        help='output directory',
        nargs=1,
        required=True
    )
    
    #absPath = os.path.abspath(.)

    args = parser.parse_args()
    dSurf = os.path.realpath(args.sub_anat[0])
    tSurf = os.path.realpath(args.sub_time[0])
    suma_surf = os.path.realpath(args.suma_surf[0])
    hemi = args.hemi[0]
    output = os.path.realpath(args.output[0])
    print(f"Decimated Surface: {dSurf}")
    print(f"Timeseries Surface: {tSurf}")
    print(f"SUMA file: {suma_surf}")
    print(f"Hemisphere: {hemi}")
    print(f"Output: {output}")

    startPath = os.getcwd()
    os.chdir(output)

    suma_align(dSurf, tSurf, suma_surf, hemi)


if __name__ == '__main__':
	main()