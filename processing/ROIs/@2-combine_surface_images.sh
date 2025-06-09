#!/bin/bash

current=`pwd`

if [ ! -e images_combined ]; then
    mkdir images_combined
fi

cd images

# for anImage in *.jpg
# do
#     newname=`echo $anImage | cut -d "_" -f 1-4`
#     mv $anImage ${newname}.jpg
# done

for aFreq in alpha beta delta highg lowg theta
do
    for aStory in pos neg
    do
        magick convert +append "result_${aFreq}_${aStory}_*.jpg" ${current}/images_combined/tmp_${aFreq}_${aStory}.jpg
        2dcat -prefix ${current}/images_combined/final_${aFreq}_${aStory}.jpg -ny 1 -crop 0 0 30 0 ${current}/images_combined/tmp_${aFreq}_${aStory}.jpg
    done
done

rm ${current}/images_combined/tmp*.jpg