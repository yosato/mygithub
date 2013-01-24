#!/bin/bash

# AddRemoveToken --charset=UTF-8 -a -f y:/yo/myResources/lex/ja_JP/artl/baidu_flat.artl -l z:/projects/MyScript_Resources/resources.src/ja_JP_org/ja_JP_jisx0213-lk-text.lex.lex -o z:/projects/MyScript_Resources/resources.src/ja_JP_org/ja_JP_jisx0213-lk-text.lex.occ -t z:/projects/MyScript_Resources/resources.src/ja_JP_org/ja_JP_jisx0213-lk-text.lex.tric  -L z:/projects/MyScript_Resources/resources.src/ja_JP/ja_JP_jisx0213-lk-text.lex.lex -O z:/projects/MyScript_Resources/resources.src/ja_JP/ja_JP_jisx0213-lk-text.lex.occ -T z:/projects/MyScript_Resources/resources.src/ja_JP/ja_JP_jisx0213-lk-text.lex.tri


###
## Ingredients: 'artl' file (frequencies and weights), original lex, original occ file, plus either bic (for lite) or tric (for full) or both
## Intermediate Output: new lex file, new occ file, new bic/tric file, as well as printing of these
## Final output: new resource
###

#Three main dirs, SB source / resource and org source to get stuff from

GitDir='z:/projects'
SBSrcRootDir=${GitDir}/MyScript_Resources/resources.src
SBResRootDir=${GitDir}/MSE_resources/resources

Lang='ja_JP'

# and these are the ones
# sandbag, resource and source
SBSrcLangDir=${SBSrcRootDir}/${Lang}
OrgSrcLangDir=${SBSrcRootDir}/${Lang}_org
SBResLangDir=${SBResRootDir}/${Lang}
  # plus the original, although eventually I had to copy this to another loc
MyExpDir=${myLingSrv}/jp_exp/ja_JP_5.0

#InitSrcDir=${MyExpDir}/v0/sources
#InitResDir=${MyExpDir}/v0/resources

Stem='ja_JP_jisx0213-lk-text'

AddOnDir=${myLingSrv}/myResources/lex/ja_JP/artl

perftesting(){

    set -x

    Opt=$1
    if [ "$Opt" = '-b' ]; then
	Stem=${2}
	StemPlus=${2}.lite
	# NC stands for n-class
	AK='ja_JP_jisx0213-ak-cur.lite.res'
    elif [ $Opt = '-t' ]; then
	Stem=$2
	StemPlus=$2
	AK='ja_JP_jisx0213-ak-cur.res'

    fi

    Vers=$3

    echo "we are perftesting ${StemPlus}.res Ver. ${Vers}, first with the new ink"

    set +x


    PerfTester -v --discard-case-variations -q 221 -r ${SBResLangDir}/${AK} -r ${SBResLangDir}/${StemPlus}.res -f y:/yo/userTest/ja_JP/ja_JP_2012-13_1/dbds-new/combined.dbd > ${MyExpDir}/v${Vers}/inkresults_v${Vers}_${StemPlus}_new || { echo 'perftester failed'; exit 1; }

#    PerfTester -v --discard-case-variations -q 221 -r ${SBResLangDir}/${AK} -r ${SBResLangDir}/${StemPlus}.res -f y:/yo/userTest/ja_JP/ja_JP_2012-13_1/dbds-new/katakana.dbd > ${MyExpDir}/v${Vers}/inkresults_v${Vers}_${StemPlus}_katakana || { echo 'perftester failed'; exit 1; }

   set +x
    echo 'now with the old ink, two dbds'

    PerfTester -v --discard-case-variations -q 221 -r ${SBResLangDir}/${AK} -r ${SBResLangDir}/${StemPlus}.res -f i:/Test_dbds/ja_JP/ja_JP-anoto2-hpr-sentence.dbd > ${MyExpDir}/v${Vers}/inkresults_v${Vers}_${StemPlus}_oldSent || { echo 'perftester failed failed'; exit 1; }

    PerfTester -v --discard-case-variations -q 221 -r ${SBResLangDir}/${AK} -r ${SBResLangDir}/${StemPlus}.res -f i:/Test_dbds/ja_JP/ja_JP-anoto2-hpr-dataformat.dbd > ${MyExpDir}/v${Vers}/inkresults_v${Vers}_${StemPlus}_oldDF || { echo 'perftester failed failed'; exit 1; }


}

# build lite resources first
# just outputting the original lex 

add_token(){

    # Five args, bic or tric -> $Opt, stem name -> $Stem, artl name -> $AddOnFP, prev vers -> $PrevVers, cur vers -> Vers

    set -x

    echo "Okay, now adding words, make sure the original sources are in the previous state" 
    echo 'stopping, press enter to proceed'; read

    Opt=$1
    if [ "$Opt" = '-b' ]; then
	Stem=${2}
	StemPlus=${2}.lite
	# NC stands for n-class
	NC=${StemPlus}.lex.bic
	AK='ja_JP_jisx0213-ak-cur.lite.res'
    elif [ $Opt = '-t' ]; then
	Stem=$2
	StemPlus=$2
	NC=${StemPlus}.lex.tric
	AK='ja_JP_jisx0213-ak-cur.res'
    else
	echo 'option missing'
	exit
    fi

    LexFN=${StemPlus}.lex.lex

    InLexFP=${OrgSrcLangDir}/${LexFN}
    OrgPrintFP=${MyExpOrg}/${StemPlus}_LMPrint.txt
    AddOnFP=$3
    InNCFP=${OrgSrcLangDir}/${NC}
    InNCMng=${OrgSrcLangDir}/${Stem}.lex.mng
    OutNCMng=${SBSrcLangDir}/${Stem}.lex.mng
    Opt=$1
    OptUpper=`echo $Opt | tr [:lower:] [:upper:]`


#    PrevVers=$4 
    Vers=$4

    set +x ; echo stopping ; read

    # copying the source to a diff dir (org), this is definitely awkward, but necessary for speed (ARToken)...
#    OrgSrcLangDir=${SBSrcRootDir}/ja_JP_org
#    cp -u ${SBSrcRootDir}/ja_JP/* ${OrgSrcLangDir} || { echo 'copy failed'; exit 1; }

    LexFN=${StemPlus}.lex.lex

    InLexFP=${OrgSrcLangDir}/${LexFN}
    OrgPrintFP=${MyExpOrg}/${StemPlus}_LMPrint.txt
    AddOnFP=$3
    InNCFP=${OrgSrcLangDir}/${NC}
    InNCMng=${OrgSrcLangDir}/${Stem}.lex.mng
    OutNCMng=${SBSrcLangDir}/${Stem}.lex.mng
    Opt=$1
    OptUpper=`echo $Opt | tr [:lower:] [:upper:]`

    #printing of 'before'
    OldPrintFP=${MyExpDir}/v${PrevVers}/${StemPlus}_LMPrint.txt
#    PrintLM -o ${OldPrintFP} -l ${InLexFP} -m ${InNCMng}
#    PrintLM -o ${OldPrintFP} -l ${InLexFP} ${Opt} ${InNCFP}


    OccFN=${StemPlus}.lex.occ
    InOccFP=${OrgSrcLangDir}/${OccFN}
    OutOccFP=${SBSrcLangDir}/${OccFN}
    OutLexFP=${SBSrcLangDir}/${LexFN}
    OutNCFP=${SBSrcLangDir}/${NC}

    # the main part, add token with artl
    AddRemoveToken --charset=UTF-8 -a -f ${AddOnFP} -l ${InLexFP} -o ${InOccFP} ${Opt} ${InNCFP} -L ${OutLexFP} -O ${OutOccFP} ${OptUpper} ${OutNCFP} #-M ${OutNCMng} #|| { echo 'ARToken failed'; exit 1; }

    #printing of 'after'
#    NewPrintFP=${MyExpDir}/v${Vers}/${StemPlus}_LMPrint.txt
#    PrintLM -o ${NewPrintFP} -l ${OutLexFP} -m ${OutNCMng}
#    PrintLM -o ${NewPrintFP} -l ${OutLexFP} ${Opt} ${OutNCFP}

    # bug, probably needs to be looked at
    rm ${SBResLangDir}/${StemPlus}.res
    rm ${SBResRootDir}/internal/ja_JP/${StemPlus}.lex.level2.res

#    ms_lrt_vo_cmd compile ja_JP_jisx0213-lk-text.lite.ardef
    ms_lrt_vo_cmd compile ja_JP--MSB_SE-packDef-internal.mk #> stdout.1
    ms_lrt_vo_cmd compile ja_JP--MSB_SE-packDef.mk #

    cp -ru ${SBResLangDir}/ ${MyExpDir}/v${Vers}/resources/
    cp -ru ${SBSrcLangDir}/ ${MyExpDir}/v${Vers}/sources/

}

#===script starts here===#

# just in case, you keep the old one

Vers=$1
Artl=$2
Start=$3

Usage='Usage:\n
add_token_evaluate.sh [NewVersName] [ArtlFNtoAdd] (ScratchOrNot)
'

if [ "$#" -lt 2 ]; then
    echo 'You need at least two args'
    echo -e $Usage
    exit
fi

# create the dirs for new version if not exists
if [ ! -d ${MyExpDir}/v${Vers}/sources ]; then
    mkdir -p ${MyExpDir}/v${Vers}/sources
fi
if [ ! -d ${MyExpDir}/v${Vers}/resources ]; then
    mkdir -p ${MyExpDir}/v${Vers}/resources
fi

    # we decide if it is lite or full by whether it's -b (biclass) or -t (triclass)


# do the light version
echo 'first we do the lite version'
#add_token -b ${Stem} ${AddOnDir}/${Artl} ${PrevVers} ${Vers} 



#perftesting -b ${Stem} ${Vers} 


# then the full one
echo 'now the full version'
add_token -t ${Stem} ${AddOnDir}/${Artl} ${PrevVers} ${Vers}

#perftesting -t ${Stem} ${Vers} 

#cp -au ${SBSrcLangDir}  ${MyExpDir}/v${Vers}/sources
#cp -au ${SBResLangDir}  ${MyExpDir}/v${Vers}/resources

#rsync -au ${SBSrcLangDir}/ ${OrgSrcLangDir}/
