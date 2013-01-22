#!/bin/bash

OldDBDs='ja_JP-anoto2-hpr-city.dbd ja_JP-anoto2-hpr-sentence.dbd ja_JP-anoto2-hpr-first_name.dbd ja_JP-anoto2-hpr-last_name.dbd ja_JP-anoto2-hpr-adress.dbd ja_JP-anoto2-hpr-sentence_mix_latin.dbd ja_JP-anoto2-hpr-state.dbd ja_JP-anoto2-hpr-email.dbd'

NewDBDs='combined.dbd words.dbd katakana.dbd sentences.dbd hiragana.dbd'

perftest_lite_full(){

set -x

DBD=$1
ResDir=$2
ResStem=$3
ResultDir=$4

set +x

echo "perftesting $DBD first full version"

PerfTester.exe -v --discard-case-variations -q 221 -r z:/projects/MyScript_Builder_SE/resources/ja_JP/ja_JP_jisx0213-ak-cur.res -r ${ResDir}'/'${ResStem}.res  -f ${DBD} > ${ResultDir}'/'inkresults_${DBD}

echo "full version test done for $DBD"

echo 'perftesting, lite version'

PerfTester.exe -v --discard-case-variations -q 221 -r z:/projects/MyScript_Builder_SE/resources/ja_JP/ja_JP_jisx0213-ak-cur.lite.res -r ${ResDir}'/'${ResStem}.lite.res  -f ${DBD} > ${ResultDir}'/'inkresults_${DBD}_lite

echo "lite version test done for $DBD"
echo -e "\n"

}

#SCRIPT STARTS HERE

# common variables
Vers=$1
ResStem=ja_JP_jisx0213-lk-text

#normal checking
if [ $# != 1 ]; then
echo 'you need a version arg'
exit
fi

# Def values
if [ "$2" = "" ]; then
    ResDir=$jpResDir
else
    ResDir=$2
fi

if [ "$3" = "" ]; then
    ResultDir='y:/yo/jp_exp/ja_JP_5.0/v'${Vers}
else
    ResultDir=$3'/v'${Vers}
fi

set -x

if [ ! -d "${ResultDir}" ]; then
    mkdir ${ResultDir}
fi

set +x
echo stopping; read

echo "On $ResultDir, resource ${ResDir}/${ResStem}. okay?"
read

echo 'first doing the old inks'

cd /cygdrive/i/Test_dbds/ja_JP

for DBD in $OldDBDs

do

echo "Testing $DBDFP with ${ResDir}/${ResStem}"

perftest_lite_full $DBD $ResDir $ResStem $ResultDir

done

echo 'now we do new inks'

cd /cygdrive/y/yo/userTest/ja_JP/ja_JP_2012-13_1/dbds

for DBD in $NewDBDs

do

perftest_lite_full $DBD $ResDir $ResStem $ResultDir

done


