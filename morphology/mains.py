#!/usr/env python3

import sys,os,imp,re,time

HomeDir=os.path.expanduser('~')
sys.path.append(HomeDir+'/links/myPython')

#FNs=['short_sentences','long_sentences','texts']
#FPs=[ HomeDir+'/links/prepDC/'+Corpus+'/'+FN+'.txt' for FN in FNs ]

import myModule
import pos_sents
imp.reload(pos_sents); imp.reload(myModule)

# switch on/off debug printing, but put it in the pos_sent module
Debug=pos_sents.Debug

#NormFails=''#Len=len(Sents)

# given the structured data ('SentAs=sentence analyses'), outputs 'bags' of the structure as just below
# WC= word chunk, WP= word/pos pair 
# SentA is a list of 2-tuples of WPs for a WC 
def mark_sents(SentAs):
    # marked/unmarked sentences, counted WPs, classified WCs are our bags
    MkdSents=set(); UnmarkedSents=set(); CtdWPs={}; CldWCs={'opt':set(),'mand':set()}
    Bags=(MkdSents,UnmarkedSents,CtdWPs,CldWCs)

    for (Cntr,SentA) in enumerate(SentAs):
        # this is a fallback for failure
        OrgBags=Bags
        USent=' '.join([ WP[0] for WP in SentA ])
        try:
            (Bags,NormP)=pos_sents.main(Cntr,SentA,Bags)
            if not NormP:
                UnmarkedSents.add(USent)
                if Debug: pos_sents.main(Cntr,SentA,Bags)

        except:
            print('\nSent '+str(Cntr+1)+'( index '+str(Cntr)+': '+USent+' FAILED\n\n')
            if Debug: 
                time.sleep(1)
                Bags=OrgBags; UnmarkedSents.add(USent)

    return Bags

# call to PoS tagger, plus pre-processing    
def pos_preprocess(FP):
    import subprocess
    print('PoS tagging in progress, this might take time...')
    PoSProc=subprocess.Popen(['java','-jar', 'jhannanum_postagger.jar', FP],shell=False,stdout=subprocess.PIPE)
    (PoSOutputF,_)=PoSProc.communicate()
    PoSOutputF=PoSOutputF.decode()
    # a bit of pre-processing
    SentAs=shallowparse_posoutput_f(PoSOutputF)
    print('... done, now we start marking'); time.sleep(2)


    return SentAs

# this is JHanNanum specific, takes the output from a file input 
def shallowparse_posoutput_f(PoSOutputF):
    SentAnalyses=[]
    # JHNN output is delimited with two lines
    PoSOutputs=PoSOutputF.split('\n\n\n')
    for PoSOutput in PoSOutputs:
        WC_WPs=shallowparse_posoutput_sent(PoSOutput)
        SentAnalyses.append(WC_WPs)
    return SentAnalyses

# this takes the output from a sentence input
def shallowparse_posoutput_sent(PoSOutput):
    # take a pair of wc and its analysis(2 lines)
    Lines=[ Line.strip() for Line in PoSOutput.splitlines() if Line.strip() ]
    Pairs=[ tuple(Lines[i:i+2]) for i in range(0, len(Lines), 2)]
    WCTagPs=[]
    for (WC,RawTags) in Pairs:
        WPPairs=[]
        for WCPStr in RawTags.split(','):
            for WPsStr in WCPStr.split('+'):
                WPPair=tuple(WPsStr.split('/'))
                WPPairs.append(WPPair)
        WCTagP=(WC,WPPairs,)
        WCTagPs.append(WCTagP)
    return WCTagPs

# writing into files of chosen data from 'bags'
def bags2files(Bags,FPStem):
    (MSents,USents,CtdWds,CldWCs)=Bags

    create_sent_files((MSents,USents),FPStem)

    create_wc_files(CldWCs,FPStem)

    create_wd_files(CtdWds,(3,8),FPStem)

def create_sent_files(Sents,FPStem):
    ''' three files created, two 'general' ones, marked / unmarked and
     'optspace' one, sentences with optional spaces with both variations, 
     i.e. with and without those spaces'''
    
    ZWNJ=pos_sents.ZWNJ
    (MSents,USents)=Sents

    myModule.write_strlist_asline(USents,FPStem+'_sent_gen_umkd.txt')
    
    StrWith='';StrWithout=''; Str2=''
    for MSent in MSents:
        if ZWNJ in MSent:
            (With,Without)=create_spacevariants(MSent)
            StrWith=StrWith+With+'\n'
#            FSw_OS.write(With+'\n')
            StrWithout=StrWithout+Without+'\n'
#            FSw_OS.write(Without+'\n')
        else:
            Str2=Str2+MSent+'\n'
#            FSw_GM.write(MSent+'\n')
    FSw_OS1=open(FPStem+'_sent_opt_taken.txt','tw')
    FSw_OS1.write(StrWith); FSw_OS1.close()
    FSw_OS2=open(FPStem+'_sent_opt_nottaken.txt','tw')
    FSw_OS2.write(StrWithout); FSw_OS2.close() 
    FSw_GM=open(FPStem+'_sent_gen_mkd.txt','tw')
    FSw_GM.write(Str2); FSw_GM.close()

def create_wd_files(CtdWds,Thrs,FPStem):
#    FreqWds={ (Wd,Freq) for (Wd,Freq) in CtdWds if Freq>10 }.keys()
    '''two files created, longer and shorter''' 
    FSw_l=open(FPStem+'_wd_longer.txt','wt')
    FSw_s=open(FPStem+'_wd_shorter.txt','wt')
    (Mid,UB)=Thrs
    for (WP,Freq) in CtdWds.items():
        Wd=WP[0]
        WLen=len(Wd)
        if WLen<=Mid and Freq>=4:
            FSw_s.write(Wd+'\n')
        elif (WLen>Mid and WLen<=UB) and Freq>=2:
            FSw_l.write(Wd+'\n')

def create_spacevariants(Sent):
    ZWNJ=pos_sents.ZWNJ
    With=re.sub(r' *%s'%ZWNJ, ' %s'%ZWNJ, Sent)
    Without=re.sub(r' %s'%ZWNJ,'%s'%ZWNJ, Sent)
    return (With,Without)


def create_wc_files(CldWCs,FPStem):
#   ''' three files created, general longer one, and two shorter ones, 
#    one with mandatory space and one with optional space
#    they should be mutually exclusive '''
    
    # mandatory /optional wcs
    MWCs=CldWCs['mand']; OWCs=CldWCs['opt']
    RedMWCs=MWCs-OWCs

    Longer=[ OWC for OWC in OWCs if len(OWC) == 9 or len(OWC) ==10 ]+[ MWC for MWC in RedMWCs if len(MWC) == 9 or len(MWC) ==10 ]
    ShorterO=[ OWC for OWC in OWCs if len(OWC) <= 8  ]
    ShorterM=[ MWC for MWC in RedMWCs if len(MWC) <= 8  ]

    FN_l=FPStem+'_wc_longer.txt'
    FN_sm=FPStem+'_wc_shorter_mand.txt'
    for (CatL,FN) in zip([Longer,ShorterM],[FN_l,FN_sm]):
        myModule.write_strlist_asline(CatL,FN)
    
    StrWith=''; StrWithout=''
    for OWC in ShorterO:
        (With,Without)=create_spacevariants(OWC)
        StrWith=StrWith+With+'\n'
        StrWithout=StrWithout+Without+'\n'

    FSw=open(FPStem+'_wc_shorter_opt_taken.txt','tw')
    FSw.write(StrWith)
    FSw.close()
    
    FSw=open(FPStem+'_wc_shorter_opt_nottaken.txt','tw')
    FSw.write(StrWithout)
    FSw.close()

def show_stats(Bags):
    print('You have bags of:')
    print('General sentence bag, '+str(len(Bags[0]))+' items')
    print('Unmarked sentence bag, '+str(len(Bags[1]))+' items')
    print('Word bag, '+str(len(Bags[2].keys()))+' items')
    print('WC with optional space, '+str(len(Bags[3]['opt']))+' items')
    print('WC with mandatory non-space, '+str(len(Bags[3]['mand']))+' items')

if __name__=='__main__':
    import argparse
    AP = argparse.ArgumentParser()
    AP.add_argument('-i', '--input-file', nargs='+', help='Input file name, needs to be full path', required=True)
    Opts = AP.parse_args()
    
    InputFP=Opts.input_file[0]
#    InputFP=HomeDir+'/links/prepDC/test.txt'
    
    if not os.path.isfile(InputFP):
        print('Specified input file does not exit, aborting'); exit()
    
    Dir=os.path.dirname(InputFP)
    FNStem=os.path.basename(InputFP).split('.')[0]
    OutputFPStem=Dir+'/'+FNStem
    
    try:
        # this calls JHanNanum and creates python object
        SentAs=pos_preprocess(InputFP)
        myModule.dump_pickle_check(SentAs, OutputFPStem+'_sentAs.pickle')
#        SentAs=myModule.load_pickle(OutputFPStem+'_sentAs.pickle')
    except:
        print('Pre-processing failed, blame either yourself (eg wrong filename), the PoS tagger or YS, in that order...\n\n')
        SentAs=pos_preprocess(InputFP)
#    myModule.dump_pickle_check(SentAs,'temp.pickle')
#    SentAs=myModule.load_pickle('temp.pickle')
    # removing ampty line
    Bags=mark_sents(SentAs)
    myModule.dump_pickle_check(Bags, OutputFPStem+'_bags.pickle')
#    Bags=myModule.load_pickle(OutputFPStem+'_bags.pickle')
    try:
        bags2files(Bags,OutputFPStem)
    except:
        print('The file writing process failed. \n\n')
        bags2files(Bags,OutputFPStem)
        
    print('Done, congrats! The files have been created in '+Dir)
    if Debug:
        show_stats(Bags)
