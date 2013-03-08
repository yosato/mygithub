#!/usr/bin/env python3

# switch on/off debug printing
Debug=True

import subprocess,imp,sys,os,sys,copy

HomeDir=os.path.expanduser('~')
Links=HomeDir+'/links'
sys.path.append(Links+'/myPython')

import myModule
imp.reload(myModule)


ZWNJ=myModule.hex_chr('200c'); ZWJ=myModule.hex_chr('200d')


#Consts={'ZWNJ':ZWNJ,'ZWJ':ZWJ,'HomeDir':HomeDir}

# combinations for mandatory non-space and optional spaces 
Combs=([(r'j..*',r'..*'),(r'paa',r'etm'),(r'p..*',r'ef'),(r'pvg',r'etm'),(r'p..*',r'ecs')],
    [(r'p..*',r'nbn'),(r'nbn',r'p..*'), 
              #(r'jc.',r'px'),
              (r'p..*', r'e.*'), # verb-modal
              (r'xs..*',r'nbn'),(r'ncp.',r'xs..*'), # verb / noun comb
              (r'nc..',r'nc..') # this is compound nouns
              ])

# this is for a single sentence
def main(Cntr,SentA,Bags):
    UnmarkedSent=''.join([ WC_WP[0]+' ' for WC_WP in SentA ])
    if Debug: print('\nDoing sent ind '+str(Cntr)+': '+UnmarkedSent)
    try:
        (WC_WPs,NormP)=normalise_tags(SentA)
    except:
        if Debug:
            (WC_WPs,NormP)=normalise_tags(SentA)
        else:
            pass
    try:
        (MkdSent,NWPs)=mark_spaces(WC_WPs)
    except:
        if Debug:
            (MkdSent,NWPs)=mark_spaces(WC_WPs)
    Bags=update_bags(Bags,MkdSent,NWPs,NormP,UnmarkedSent)
    return (Bags,NormP)


# tag (wc_wp) normalisation-----------------------------------------------

def normalise_tags(OrgWC_WPs):
    WC_WPs=copy.deepcopy(OrgWC_WPs)
    NWPs=[]
    WC_WPs=purge_bad_wps(WC_WPs)
    for WC_WP in WC_WPs:
        try:
            if Debug: print('Normalising WC: '); print(WC_WP)
            NWP=normalise_tag0(WC_WP)
            if Debug: sys.stdout.write('  ... and normalised: '); print(NWP)
            NWPs.append(NWP)
            
        except:
            sys.stdout.write('Failing normalising: '); print(WC_WP)
            NormP=False

    
    NormP=normalisation_ok_p(WC_WPs,NWPs)
    
    return (NWPs,NormP)


def normalise_tag0(OrgWCTagPair):
  #  import normalise
    (WC,WPs)=copy.deepcopy(OrgWCTagPair)
    if WC==''.join([ WP[0] for WP in WPs ]):
        NewWPs=WPs
    else:
        WNums=[ len(WP[0]) for WP in WPs ]
        Ws=''.join([ WP[0] for WP in WPs ])
        Ps=[ WP[1] for WP in WPs ]
        NewWPs=normalise_unequaltag(WC,Ws,WNums,Ps)

    return NewWPs

def normalise_unequaltag(WC,Ws,WNums,Ps):
    NewWPs=[]

    CumWCChars='';  WCChar=WC[0];WsChar=Ws[0]
    while WC and WCChar==WsChar:
        # cumulates it
        CumWCChars=CumWCChars+WCChar

        if len(CumWCChars)==WNums[0]:
            WNums.pop(0)
            NewWPs.append((CumWCChars,Ps.pop(0)))
            CumWCChars=''
            
        WC=WC[1:]; Ws=Ws[1:]
        WCChar=WC[0];WsChar=Ws[0]



    if CumWCChars:
        NewWPs.append((CumWCChars+WC[0],Ps.pop(0)))
        WC=WC[1:]

    NewWPsRev=[]
    CumWCCharsRev=''; WCCharRev=WC[-1];WsCharRev=Ws[-1]
    while WC and WCCharRev==WsCharRev:
        CumWCCharsRev=WCCharRev+CumWCCharsRev
        if len(CumWCCharsRev)==WNums[-1]:
            WNums.pop(-1)
            NewWPsRev.append((CumWCCharsRev,Ps.pop(-1)))
            CumWCCharsRev=''
        WC=WC[:-1]; Ws=Ws[:-1]
        WCCharRev=WC[-1];WsCharRev=Ws[-1]

        

    if CumWCCharsRev:
        NewWPsRev.append((CumWCCharsRev,Ps.pop(-1)))
    NewWPsRev.reverse()

    if WC and Ps:
        NewWPs.append((WC,Ps.pop(0)))

    NewWPs.extend(NewWPsRev)
    
    return NewWPs    


def normalise_tag(OrgWCTagPair):
    (WC,Tag)=copy.deepcopy(OrgWCTagPair)
    NTag=[]
    # as long as the surface word is the same as the analysed, leave it
    while Tag:
        WP=Tag[0]
#        if len(WP)==2:
        (Wd0,PoS)=WP
        if WC.startswith(Wd0):
            NTag.append((Wd0,PoS))
            WC=WC[len(Wd0):]
        else:
            break
        Tag.pop(0)

    # this is when the surface and the analysed differ
    if Tag:
        AnalysisSum=sum([ len(WP[0]) for WP in Tag ])
        if len(WC)==AnalysisSum: # this is when no contraction occurs
            NTag.extend(split_accordingly(Tag,WC))
        else:
            NTag.extend(merge_wc(WC,Tag))
            

    return NTag


def merge_wc(WC,OrgWPs):
    NewWPs=[]; WPs=copy.deepcopy(OrgWPs)
#    AWds=[ WP[0] for WP in WPs ]
    while WPs:
        WP=WPs.pop(0); (AWd,PoS)=WP
        CumWC=''; DiffFnd=False
        for WCChar,AWdChar in zip(WC,AWd):
            if WCChar != AWdChar:
                DiffFnd=True
            CumWC=CumWC+WCChar; WC=WC[1:]
        if DiffFnd:
            NxtWP=WPs[0]
            RedNxtWd=NxtWP[0][1:]
            if RedNxtWd=='':
                WPs.pop(0)
            else:
                WPs[0]=(RedNxtWd,WPs[0][1])
            NewWP=(CumWC,WP[1])
        else:
            NewWP=WP
        NewWPs.append(NewWP)
            
    return NewWPs

def split_accordingly(Tag,WC):
    NewTag=[]
    Cnts=[ len(WP[0]) for WP in Tag ]
    Cum=0
    for (Cntr,Cnt) in enumerate(Cnts):
        Wd=WC[Cum:Cum+Cnt]; P=Tag[Cntr][1]
        NewTag.append((Wd,P))
        Cum=Cum+Cnt
    return NewTag

def purge_bad_wps(WC_WPs):
#    WC_WPs= [ WC_WP for WC_WP in WC_WPs if len(WC_WP)==2 d WC_WP[0]!='/' ]
    for WC_WP in WC_WPs:
        WPs=WC_WP[1]
        if ('','sp') in WPs:
            WPs[WPs.index(('','sp'))]=(',','sp')
        if ('',) in WPs:
            WPs.remove(('',))
    return WC_WPs
#        if (',','sp') in WPs:
#            WPs[WPs.index(('','sp'))]=('/','sp')

def normalisation_ok_p(WC_WPs,NWPs):
    OrgStr=''.join([ WC_WP[0] for WC_WP in WC_WPs ])
    NewStr=''.join([ WP[0] for WP in myModule.flatten_list(NWPs) ])
    if OrgStr==NewStr:
        Bool=True
    else:
        Bool=False
    return Bool

# space marking-------------------------------------


def mark_spaces(NTags):
    Str=''
    WPs=myModule.flatten_list(NTags)

    LstWP=('','')
    # and this is WC level
    for (Cntr,NTag) in enumerate(NTags):
#        if Debug: sys.stdout.write('Up to WC'+str(Cntr+1))
        # this part is to determine whether the space between two wcs is optional or not
        # so, the first one is ignored, 
        if Cntr==0:
            Space=''
        # and from the second one, the top tag of it and the last tag of the previous one are compared
        else:
            if optional_space_p(LstWP,NTag[0]):
                Space=' '+ZWNJ
            else:
                Space=' '
               
        # and this is the intra-WC part
        WCStr=mark_intrawc(NTag)
        # then mark the space plus the WC accordingly
        Str=Str+Space+WCStr
#        if Debug and Cntr==len(NTags)-1:
#                sys.stdout.write('Marked: '); print([Str])
        # the last one of the current tag is stored as the 'previous' tag
        LstWP=NTag[-1]
    return (Str,WPs)


def mark_intrawc(NTag):
    try:
        PrevWP=('','')
        for (Cntr,WP) in enumerate(NTag):
            (Wd,_)=WP
            if Cntr==0:
                Str=Wd
            elif optional_space_p(PrevWP,WP): 
        #PoS.startswith('j'):
                Str=Str+ZWNJ+Wd
            else:
                Str=Str+ZWJ+Wd
            PrevWP=WP
    except:
        mark_intrawc(NTag)

    return Str

def optional_space_p(WP1,WP2):
    import re
    (MandCombs,OptCombs)=Combs
    (_Wd1,PoS1)=WP1;   (_Wd2,PoS2)=WP2
    for MComb in MandCombs:
        if re.match(MComb[0], PoS1) and re.match(MComb[1], PoS2):
                Val=False; break
    else:
        Val=False
        for OComb in OptCombs:
            if re.match(OComb[0], PoS1) and re.match(OComb[1], PoS2):
                Val=True; break
    return Val

def split_and_glue_end(Tag,WC):
    NewTag=split_accordingly(Tag[:-2],WC)
    LstStr=WC[-2:]
    NewTag.append((LstStr,Tag[-2][1]))
    return NewTag


def update_bags(Bags,MkdSent,NWPs,NormP,UnmarkedSent):
    (MkdSents,UnmarkedSents,CtdWPs,CldWCs)=Bags
    if NormP:
        MkdSents.add(MkdSent)
        update_wdstats(NWPs,CtdWPs)
        process_wcs(MkdSent,NWPs,CldWCs)
    else:
        UnmarkedSents.add(UnmarkedSent)

    return Bags



def update_wdstats(WPs,CtdWPs):
    for WP in WPs:
        if WP in CtdWPs.keys():
            CtdWPs[WP]=CtdWPs[WP]+1
        else:
            CtdWPs[WP]=1

def process_wcs(MkdSent,NTags,CldWCs):
    for WC in MkdSent.split():
        if WC.find(ZWNJ)!=-1:
            CldWCs['opt'].add(WC)
        if WC.find(ZWJ)!=-1:
            CldWCs['mand'].add(WC)

# ===== old one, this does pre-processing for each sentence

'''
 
def main1(Cntr,Sent,Bags,Len):
    print('\nSentence being processed, Index '+str(Cntr)+' (of '+str(Len)+'): '+Sent)
    
    (MkdSent,NWPs,NormP)=main_processes(Sent)
    # data updates, if normalisation goes okay
    if NormP:
        Bags=update_bags(Bags,MkdSent,NWPs)

    return (Bags,NormP)

def main_processes(Sent):
    if Debug: sys.stdout.write('PoS tagging...')
    WC_WPs=pos_preprocess(Sent)
    
    if Debug: print(' done'); sys.stdout.write('Now normalising...')
    (NWPs,NormP)=normalise_tags(WC_WPs)
    
    if NormP:
        if Debug: print('Now marking spaces...')
        (MkdSent,NWPs)=mark_spaces(NWPs)
    
        sys.stdout.write('Marked: '); print([MkdSent])
    else:
        MkdSent=''; NWPs=[]; UnmarkedSent=Sent
        print('Normalisation check failed for '+Sent+', skipping')
    
    return (MkdSent,NWPs,NormP)

'''
